# copyright 2003-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.

from logilab.common.testlib import TestCase, unittest_main

from cubicweb import ObjectNotFound
from cubicweb import Unauthorized
from cubicweb.devtools import BASE_URL
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.req import RequestSessionAndConnectionBase


class RequestTC(TestCase):
    def test_rebuild_url(self):
        rebuild_url = RequestSessionAndConnectionBase(None).rebuild_url
        self.assertEqual(
            rebuild_url("http://logilab.fr?__message=pouet", __message="hop"),
            "http://logilab.fr?__message=hop",
        )
        self.assertEqual(
            rebuild_url("http://logilab.fr", __message="hop"),
            "http://logilab.fr?__message=hop",
        )
        self.assertEqual(
            rebuild_url("http://logilab.fr?vid=index", __message="hop"),
            "http://logilab.fr?__message=hop&vid=index",
        )

    def test_build_url(self):
        req = RequestSessionAndConnectionBase(None)
        req.from_controller = lambda: "view"
        req.relative_path = lambda includeparams=True: None
        req.base_url = lambda: BASE_URL
        self.assertEqual(req.build_url(), f"{BASE_URL}view")
        self.assertEqual(req.build_url(None), f"{BASE_URL}view")
        self.assertEqual(req.build_url("one"), f"{BASE_URL}one")
        self.assertEqual(req.build_url(param="ok"), f"{BASE_URL}view?param=ok")
        self.assertRaises(AssertionError, req.build_url, "one", "two not allowed")
        self.assertRaises(AssertionError, req.build_url, "view", test=None)

    def test_ensure_no_rql(self):
        req = RequestSessionAndConnectionBase(None)
        self.assertEqual(req.ensure_ro_rql("Any X WHERE X is CWUser"), None)
        self.assertEqual(req.ensure_ro_rql("  Any X WHERE X is CWUser  "), None)
        self.assertRaises(
            Unauthorized, req.ensure_ro_rql, 'SET X login "toto" WHERE X is CWUser'
        )
        self.assertRaises(
            Unauthorized,
            req.ensure_ro_rql,
            '   SET X login "toto" WHERE X is CWUser   ',
        )


class RequestCWTC(CubicWebTC):
    def test_base_url(self):
        base_url = self.config["base-url"]
        with self.admin_access.repo_cnx() as session:
            self.assertEqual(session.base_url(), base_url)

    def test_view_catch_ex(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('CWUser X WHERE X login "hop"')
            self.assertEqual(req.view("oneline", rset, "null"), "")
            self.assertRaises(ObjectNotFound, req.view, "onelinee", rset, "null")

    def test_find(self):
        with self.admin_access.web_request() as req:
            req.create_entity(
                "CWUser",
                login="cdevienne",
                upassword="cdevienne",
                surname="de Vienne",
                firstname="Christophe",
                in_group=req.find("CWGroup", name="users").one(),
            )

            req.create_entity(
                "CWUser",
                login="adim",
                upassword="adim",
                surname="di mascio",
                firstname="adrien",
                in_group=req.find("CWGroup", name="users").one(),
            )

            rset = req.find("CWUser", login="cdevienne")
            self.assertEqual(
                rset.printable_rql(), 'Any X WHERE X is CWUser, X login "cdevienne"'
            )
            u = rset.one()
            self.assertEqual(u.firstname, "Christophe")

            users = list(req.find("CWUser").entities())
            self.assertEqual(len(users), 4)

            groups = list(req.find("CWGroup", reverse_in_group=u).entities())
            self.assertEqual(len(groups), 1)
            self.assertEqual(groups[0].name, "users")

            rset = req.find("CWUser", in_group=groups[0])
            self.assertEqual(
                rset.printable_rql(),
                "Any X WHERE X is CWUser, X in_group A, "
                "A eid {}".format(groups[0].eid),
            )
            users = list(rset.entities())
            self.assertEqual(len(users), 2)

            with self.assertRaisesRegex(
                KeyError, "^'chapeau not in CWUser subject relations'$"
            ):
                req.find("CWUser", chapeau="melon")

            with self.assertRaisesRegex(
                KeyError, "^'buddy not in CWUser object relations'$"
            ):
                req.find("CWUser", reverse_buddy=users[0])

            with self.assertRaisesRegex(
                NotImplementedError, "^in_group: list of values are not supported$"
            ):
                req.find("CWUser", in_group=[1, 2])

    def test_exists(self):
        with self.admin_access.web_request() as req:
            user_group = req.find("CWGroup", name="users").one()
            req.create_entity(
                "CWUser",
                login="rms",
                upassword="gnu",
                firstname="Richard",
                surname="Stallman",
                in_group=user_group,
            )

            self.assertFalse(req.exists("CWUser", login="not_in_the_db"))
            self.assertTrue(req.exists("CWUser", login="rms"))
            self.assertTrue(req.exists("CWUser", login="rms", in_group=user_group))


if __name__ == "__main__":
    unittest_main()
