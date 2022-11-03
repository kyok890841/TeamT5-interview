import unittest
from flask import url_for
from flask_testing import TestCase
from app import create_app, db
import json
 
class SettingBase(TestCase):
    def create_app(self):
        return create_app("testing")
 
      # 在運行測試之前會先被執行
    def setUp(self):
        db.create_all()
        self.username = "test@a.com"
        self.passwords = "666666"
        self.role = 0
 
      # 在結束測試時會被執行
    def tearDown(self):
        db.session.remove()
        db.drop_all()
 
      # signup 是測試時很常會被用到的功能，所以寫成函式，可以重複利用
    def signup(self):
        response = self.client.post(url_for('api.users'),
                                    follow_redirects=True,
                                    json={
                                        "username": self.username,
                                        "password": self.passwords,
                                        "role": self.role
                                    })
        return response
 
 
# 這邊繼承剛剛的寫的 SettingBase class，接下來會把測試都寫在這裡
class CheckUserAndLogin(SettingBase):
    def test_signup(self):
        response = self.signup()
        self.assertEqual(response.status_code, 200)
 
    def test_signup_400(self):
        # 測試密碼少於六位數
        self.passwords = '123'
        response = self.signup()
        self.assertEqual(response.status_code, 400)
 
    def test_signup_422(self):
        # 測試重複註冊
        response = self.signup()
        response = self.signup()
        self.assertEqual(response.status_code, 422)
 
 
if __name__ == '__main__':
    unittest.main()