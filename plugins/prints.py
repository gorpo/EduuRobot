# Copyright (C) 2018-2019 Amano Team <contact@amanoteam.ml>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import re
import time

import aiohttp

from config import bot


async def prints(msg):
    if msg.get('text'):
        if msg['text'].startswith('/print ') or msg['text'].startswith('!print '):
            try:
                sent = await bot.sendMessage(msg['chat']['id'], 'Tirando print...',
                                             reply_to_message_id=msg['message_id'])
                ctime = time.time()
                if re.match(r'^[a-z]+://', msg['text'][7:]):
                    url = msg['text'][7:]
                else:
                    url = 'http://' + msg['text'][7:]
                async with aiohttp.ClientSession() as session:
                    r = await session.post("https://api.olixao.ml/print", data=dict(q=url))
                    file = await r.read()
                    with open(f'{ctime}.png', 'wb') as f:
                        f.write(file)

                await bot.sendPhoto(msg['chat']['id'], open(f'{ctime}.png', 'rb'),
                                    reply_to_message_id=msg['message_id'])
                await bot.deleteMessage((msg['chat']['id'], sent['message_id']))
            except Exception as e:
                await bot.editMessageText((msg['chat']['id'], sent['message_id']),
                                          f'Ocorreu um erro ao enviar a print, favor tente mais tarde.\nErro: {e}')
            finally:
                try:
                    os.remove(f'{ctime}.png')
                except FileNotFoundError:
                    pass
            return True
