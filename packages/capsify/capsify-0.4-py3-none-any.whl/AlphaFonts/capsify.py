ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
ALL_CAPS = "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"

def capsify(text: str, ignore_delimiter = '*') -> str:
    if ignore_delimiter.lower() in ALPHABETS:
        raise Exception("Delimiter cannot be an alphabet.")
    if text.count(ignore_delimiter) % 2 != 0:
       raise Exception("Invalid Delimiters placement for capsify ignore case.")
    txt = ""
    ignore = False
    for x in text:
        if x == ignore_delimiter:
            ignore = not ignore
            continue
        if ignore:
            txt += x
            continue
        if x.lower() in ALPHABETS:
            ind = ALPHABETS.index(x.lower())
            txt += ALL_CAPS[ind]
        else:
            txt += x
    return txt
  
async def acapsify(text: str) -> str:
    return capsify(text)