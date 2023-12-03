async def generate_question(data, admin=True):
    q = await generate_block(data, 'q')
    a1 = await generate_block(data, 'a1')
    a2 = await generate_block(data, 'a2')
    a3 = await generate_block(data, 'a3')
    a4 = await generate_block(data, 'a4')

    ticked = lambda x: '✅' if data[x]['correct'] and admin else ''


    q = f'{q}\n\n' if q else ''
    a1 = f'<b>A.</b> {ticked("a1")}{a1}\n\n' if a1 else ''
    a2 = f'<b>B.</b> {ticked("a2")}{a2}\n\n' if a2 else ''
    a3 = f'<b>C.</b> {ticked("a3")}{a3}\n\n' if a3 else ''
    a4 = f'<b>D.</b> {ticked("a4")}{a4}\n\n' if a4 else ''

    return f"{q}{a1}{a2}{a3}{a4}"


async def generate_block(data, what):
    text = data[what]['text']
    video = data[what]['video']
    image = data[what]['image']
    audio = data[what]['audio']
    file = data[what]['file']

    text = text if text else ''
    video = f"<a href='{video}'>video</a>" if video else ''
    photo = f"<a href='{image}'>rasm</a>" if image else ''
    audio = f"<a href='{audio}'>Audio</a>" if audio else ''
    file = f"<a href='{file}'>File</a>" if file else ''.strip()
    supplement = []
    if photo: supplement.append(photo)
    if video: supplement.append(video)
    supplement_text = f"\n\nQuyida {' va '.join(supplement)} berilgan" if photo or video else ''
    return f"{text}{supplement_text}"
