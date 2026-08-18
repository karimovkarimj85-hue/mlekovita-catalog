"""Phone-sized catalog PDF from the site: prices in сум/шт."""

from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "catalog.pdf"
FONTS = Path(r"C:\Windows\Fonts")
W, H = 420, 790

CREAM = (0.973, 0.941, 0.878)
PAPER = (1, 0.976, 0.933)
CHOCO = (0.220, 0.157, 0.094)
GOLD = (0.914, 0.765, 0.518)
GOLD2 = (0.851, 0.769, 0.647)
MUTED = (0.604, 0.514, 0.408)
INK = (0.227, 0.180, 0.133)
GREEN = (0.184, 0.541, 0.227)
RED = (0.761, 0.122, 0.227)
NAVY = (0.110, 0.239, 0.431)
WHITE = (1, 1, 1)

PRODUCTS = [
    {
        "img": ROOT / "assets/products/cream-12-500.png",
        "fat": "12%",
        "volume": "500 мл",
        "tag": "Кулинарные",
        "price": "36 000",
        "tone": GREEN,
        "points": [
            "Супы, соусы, запеканки, салаты",
            "К кофе, десертам и выпечке",
            "Нежная кремовая текстура",
        ],
    },
    {
        "img": ROOT / "assets/products/cream-30-500.png",
        "fat": "30%",
        "volume": "500 мл",
        "tag": "Десертные",
        "price": "38 000",
        "tone": RED,
        "points": [
            "Из отборного молочного сырья",
            "Для взбивания в пышные сливки",
            "Кремы, торты и десерты",
        ],
    },
    {
        "img": ROOT / "assets/products/cream-36-500.png",
        "fat": "36%",
        "volume": "500 мл",
        "tag": "Десертные",
        "price": "40 000",
        "tone": NAVY,
        "points": [
            "Для взбивания в густые сливки",
            "Основа для кремов и муссов",
            "Насыщенный сливочный вкус",
        ],
    },
    {
        "img": ROOT / "assets/products/cream-30-1l.png",
        "fat": "30%",
        "volume": "1 л",
        "tag": "Десертные",
        "price": "60 000",
        "tone": RED,
        "points": [
            "Ультрапастеризованные 30%",
            "Для сладких и несладких блюд",
            "Удобный объём для HoReCa",
        ],
    },
]


def font(name: str) -> str:
    return str(FONTS / name)


def round_rect(page, rect, fill, color=None, radius=0.08, width=0.4):
    page.draw_rect(rect, fill=fill, color=color or fill, width=width, radius=radius)


def text(page, xy, value, fontsize, fontname, color, archive):
    page.insert_text(xy, value, fontsize=fontsize, fontname=fontname, fontfile=archive, color=color)


def wrapped(page, rect, value, fontsize, fontname, archive, color, leading=None):
    page.insert_textbox(
        rect,
        value,
        fontsize=fontsize,
        fontname=fontname,
        fontfile=archive,
        color=color,
        align=pymupdf.TEXT_ALIGN_LEFT,
    )


def cover(doc):
    page = doc.new_page(width=W, height=H)
    page.draw_rect(page.rect, fill=CREAM, color=CREAM)
    header = pymupdf.Rect(18, 18, W - 18, 250)
    round_rect(page, header, CHOCO, radius=0.06)
    page.draw_circle((W - 28, 36), 70, fill=(0.29, 0.20, 0.15), color=(0.29, 0.20, 0.15))

    text(page, (36, 46), "EURO BRANDS GROUP", 8, "f1", GOLD2, font("segoeui.ttf"))
    text(page, (34, 88), "Сливки", 34, "f2", GOLD, font("georgia.ttf"))
    text(page, (34, 128), "Mlekovita", 34, "f3", GOLD, font("georgiai.ttf"))
    wrapped(
        page,
        pymupdf.Rect(34, 148, 300, 190),
        "Нежность, проверенная временем — премиальные сливки прямо с завода-производителя",
        10,
        "f3",
        font("georgiai.ttf"),
        GOLD2,
    )
    wrapped(
        page,
        pymupdf.Rect(34, 198, 360, 230),
        "Официальный дистрибьютор MLEKOVITA (Польша) · Коммерческое предложение",
        8.5,
        "f1",
        font("segoeui.ttf"),
        (0.788, 0.686, 0.549),
    )

    text(page, (24, 278), "Уважаемые партнёры,", 16, "f2", CHOCO, font("georgia.ttf"))
    wrapped(
        page,
        pymupdf.Rect(24, 292, W - 24, 372),
        "Euro Brands Group поставляет сливки MLEKOVITA напрямую с завода в Польше. "
        "Продукция с сертификатами ЕС и Халяль, для розницы и HoReCa. "
        "Стабильный склад, гибкие условия и индивидуальные скидки.",
        10,
        "f4",
        font("segoeui.ttf"),
        INK,
    )

    benefits = [
        "Гарантированное качество и подлинность",
        "Цены от официального дистрибьютора",
        "Гибкие условия и индивидуальные скидки",
        "Стабильные поставки и наличие на складе",
    ]
    for i, line in enumerate(benefits):
        col, row = i % 2, i // 2
        x0 = 18 + col * 196
        y0 = 386 + row * 64
        box = pymupdf.Rect(x0, y0, x0 + 188, y0 + 56)
        round_rect(page, box, WHITE, color=(0.89, 0.82, 0.73), radius=0.14)
        page.draw_circle((x0 + 18, y0 + 28), 9, fill=CHOCO, color=CHOCO)
        text(page, (x0 + 14.5, y0 + 32), "✓", 9, "f5", PAPER, font("arialbd.ttf"))
        wrapped(page, pymupdf.Rect(x0 + 34, y0 + 10, box.x1 - 8, box.y1 - 8), line, 9, "f4", font("segoeui.ttf"), INK)

    contact = pymupdf.Rect(18, 528, W - 18, 678)
    round_rect(page, contact, CHOCO, radius=0.06)
    text(page, (34, 556), "Свяжитесь с нами", 18, "f2", PAPER, font("georgia.ttf"))
    lines = [
        "Телефон   95 016 03 30",
        "WhatsApp  +998 95 016 03 30",
        "E-mail    info@eurobrandsgroup.uz",
        "Сайт      eurobrandsgroup.uz",
    ]
    for i, line in enumerate(lines):
        text(page, (34, 582 + i * 18), line, 10, "f4", GOLD2, font("segoeui.ttf"))
    wrapped(
        page,
        pymupdf.Rect(34, 650, W - 34, 672),
        "С уважением, команда EURO BRANDS GROUP · Директор — Абдукаюмов А.А.",
        8,
        "f3",
        font("georgiai.ttf"),
        GOLD,
    )

    wrapped(
        page,
        pymupdf.Rect(24, 694, W - 24, 770),
        "Республика Узбекистан, г. Ташкент, Сергелийский район, Aeroport hududi ko'chasi, 118/119\n"
        "Р/с № 2020 8000 9054 0878 5001 в АКИБ «Ипотека Банк», Шайхонтохурский филиал\n"
        "МФО 00425, ИНН 308619234, ОКЭД 46900",
        7.2,
        "f4",
        font("segoeui.ttf"),
        MUTED,
    )


def products(doc):
    page = doc.new_page(width=W, height=H)
    page.draw_rect(page.rect, fill=CREAM, color=CREAM)
    head = pymupdf.Rect(18, 16, W - 18, 78)
    round_rect(page, head, CHOCO, radius=0.12)
    text(page, (32, 42), "Сливки Mlekovita", 18, "f2", PAPER, font("georgia.ttf"))
    text(page, (32, 62), "Ультрапастеризованные · из отборного сырья · цена за шт", 8.5, "f4", GOLD2, font("segoeui.ttf"))

    gap, left, top = 10, 18, 92
    card_w = (W - 36 - gap) / 2
    card_h = 318
    for i, item in enumerate(PRODUCTS):
        col, row = i % 2, i // 2
        x0 = left + col * (card_w + gap)
        y0 = top + row * (card_h + gap)
        box = pymupdf.Rect(x0, y0, x0 + card_w, y0 + card_h)
        round_rect(page, box, WHITE, color=(0.89, 0.82, 0.73), radius=0.05)
        stripe = pymupdf.Rect(x0, y0, box.x1, y0 + 7)
        round_rect(page, stripe, item["tone"], color=item["tone"], radius=0.2)

        photo = pymupdf.Rect(x0 + 10, y0 + 16, box.x1 - 10, y0 + 150)
        page.draw_rect(photo, fill=PAPER, color=PAPER, radius=0.08)
        page.insert_image(photo, filename=str(item["img"]), keep_proportion=True)

        text(page, (x0 + 12, y0 + 168), "Сливки Mlekovita", 9.5, "f2", CHOCO, font("georgiab.ttf"))
        text(page, (x0 + 12, y0 + 182), f"{item['fat']} · {item['volume']}", 8, "f4", MUTED, font("segoeui.ttf"))
        tag = pymupdf.Rect(x0 + 12, y0 + 188, x0 + 88, y0 + 204)
        round_rect(page, tag, (0.941, 0.886, 0.800), color=(0.941, 0.886, 0.800), radius=0.4)
        text(page, (x0 + 18, y0 + 199), item["tag"], 7, "f4", CHOCO, font("segoeui.ttf"))

        y = y0 + 214
        for point in item["points"]:
            wrapped(page, pymupdf.Rect(x0 + 12, y, box.x1 - 10, y + 22), "• " + point, 7.2, "f4", font("segoeui.ttf"), INK)
            y += 18

        price = pymupdf.Rect(x0 + 8, box.y1 - 40, box.x1 - 8, box.y1 - 8)
        round_rect(page, price, CHOCO, radius=0.18)
        text(page, (price.x0 + 10, price.y0 + 22), item["price"], 14, "f2", GOLD, font("georgiab.ttf"))
        wrapped(
            page,
            pymupdf.Rect(price.x1 - 78, price.y0 + 6, price.x1 - 8, price.y1 - 4),
            "сум / шт\nс НДС",
            7,
            "f4",
            font("segoeui.ttf"),
            GOLD2,
        )

    text(page, (24, 770), "95 016 03 30  ·  info@eurobrandsgroup.uz  ·  eurobrandsgroup.uz", 8, "f4", MUTED, font("segoeui.ttf"))


def main():
    doc = pymupdf.open()
    cover(doc)
    products(doc)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT, deflate=True, garbage=4)
    doc.close()
    print("wrote", OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
