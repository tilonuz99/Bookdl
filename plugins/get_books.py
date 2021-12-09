from hashlib import md5
from re import findall

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument

from Bookdl.pdfdrive import search, genereate_url
from database.model import Books
from Bookdl.save import save
from aiofiles.os import remove

@Client.on_message(filters.command('start'))
async def send_welcome(client: Client, message: Message):
    await message.reply_text("Kitoblar olami)")

@Client.on_message(filters.text & filters.private)
async def search_book(client: Client, message: Message):
    results = await search(message.text)
    if len(results) == 0:
        await message.reply_text("Hech narsa topilmadi!")
        return

    searched_results = "Natijalar: \n\n"
    i = 0
    keyboard = []
    
    for x, result in enumerate(results.values()):
        title, url = result
        hash_string = md5(url.encode()).hexdigest()
        exist_db = await Books.filter(hash_id=hash_string).exists()
        if not exist_db:
            await Books.create(book_url=url, hash_id=hash_string, title=title.replace("PDFDrive", '@BOOKSBOt'))
        i += 1
        
        keyboard.append(InlineKeyboardButton(text=i, callback_data=f'd-{hash_string}'))
        
        searched_results += f"{i}. <b>{title}</b>\n"

    keyboard = [keyboard[p:p + 5] for p in range(0, len(keyboard), 5)]
    await message.reply_text(searched_results, parse_mode='html', reply_markup=InlineKeyboardMarkup(list(keyboard)))


@Client.on_callback_query(filters.regex(r"^d-(.*)"), group=1)
async def down_lib(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    hash_string = query.matches[0].group(1)
    get_book = await Books.filter(hash_id=hash_string).first()
    if not get_book:
        await query.message.delete()
        await query.answer("Kitob nomini qayta yuboring...", show_alert=True)
        return
    if get_book.file_id is not None:
        await client.send_document(user_id, get_book.file_id, caption=get_book.title)
        return
    book_url, file_info = await genereate_url(get_book.book_url)
    
    file_size, size_type = file_info[2].split(" ")[0], file_info[2].split(" ")[1]
    file_size = float(file_size.replace(',', '.'))

    if (file_size < 20.0 and size_type in ['MB', 'mb', 'Mb']) or (size_type in ['KB', 'kb', 'Kb']):
        try:
            file_id = (await client.send_document(user_id, book_url, file_name=f"@BooksPortalBot_{get_book.title}.pdf", caption=get_book.title)).document.file_id
            await Books.filter(hash_id=hash_string).update(file_id=file_id)
        except Exception as e:
            file_path = f"{get_book.hash_id}_{user_id}.pdf"
            file_location = await save(file_path, book_url)
            if file_location:
                try:
                    file_id = (await client.send_document(user_id, file_location, file_name=f"@BooksPortalBot_{get_book.title}.pdf", caption=get_book.title)).document.file_id
                    await Books.filter(hash_id=hash_string).update(file_id=file_id)
                except:
                    await query.message.reply_text("Kitobni yuborib bo'lmadi!")
            else:
                await query.message.reply_text("Kitobni yuborib bo'lmadi!")
            try:
                await remove(file_location)
            except:
                pass
    else:
        file_path = f"{get_book.hash_id}_{user_id}.pdf"
        file_location = await save(file_path, book_url)
        if file_location:
            try:
                file_id = (await client.send_document(user_id, file_location, file_name=f"@BooksPortalBot_{get_book.title}.pdf", caption=get_book.title)).document.file_id
                await Books.filter(hash_id=hash_string).update(file_id=file_id)
            except:
                await query.message.reply_text("Kitobni yuborib bo'lmadi!")
        else:
            await query.message.reply_text("Kitobni yuborib bo'lmadi!")
        try:
            await remove(file_location)
        except:
            pass

