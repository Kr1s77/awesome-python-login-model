from __future__ import print_function

import argparse
import requests
import pyquery


def login(session, email, password):
    """
    获取cookie
    """
    response = session.get('https://m.facebook.com')

    # 尝试登陆
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)

    if 'c_user' in response.cookies:
        # 说明登陆成功
        homepage_resp = session.get('https://m.facebook.com/home.php')

        dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
        fb_dtsg = dom('input[name="fb_dtsg"]').val()

        return fb_dtsg, response.cookies['c_user'], response.cookies['xs']
    else:
        return False


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Login to Facebook')
    parser.add_argument('email', help='Email address')
    parser.add_argument('password', help='Login password')

    args = parser.parse_args()

    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    })

    fb_dtsg, user_id, xs = login(session, args.email, args.password)

    if user_id:
        print('{0}:{1}:{2}'.format(fb_dtsg, user_id, xs))
    else:
        print('Login Failed')
