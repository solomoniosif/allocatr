from datetime import date
from calendar import monthrange
from dateutil.relativedelta import relativedelta


COLOR_PALETTE = [
    # Red
    ("#FDE8E8", "red-100"),
    ("#FBD5D5", "red-200"),
    ("#F8B4B4", "red-300"),
    ("#F98080", "red-400"),
    ("#F05252", "red-500"),
    ("#E02424", "red-600"),
    ("#C81E1E", "red-700"),
    ("#9B1C1C", "red-800"),
    # Yellow
    ("#FDF6B2", "yellow-100"),
    ("#FCE96A", "yellow-200"),
    ("#FACA15", "yellow-300"),
    ("#E3A008", "yellow-400"),
    ("#C27803", "yellow-500"),
    ("#9F580A", "yellow-600"),
    ("#8E4B10", "yellow-700"),
    ("#723B13", "yellow-800"),
    # Green
    ("#DEF7EC", "green-100"),
    ("#BCF0DA", "green-200"),
    ("#84E1BC", "green-300"),
    ("#31C48D", "green-400"),
    ("#0E9F6E", "green-500"),
    ("#057A55", "green-600"),
    ("#046C4E", "green-700"),
    ("#03543F", "green-800"),
    # Blue
    ("#E1EFFE", "blue-100"),
    ("#C3DDFD", "blue-200"),
    ("#A4CAFE", "blue-300"),
    ("#76A9FA", "blue-400"),
    ("#3F83F8", "blue-500"),
    ("#1C64F2", "blue-600"),
    ("#1A56DB", "blue-700"),
    ("#1E429F", "blue-800"),
    # Indigo
    ("#E5EDFF", "indigo-100"),
    ("#CDDBFE", "indigo-200"),
    ("#B4C6FC", "indigo-300"),
    ("#8DA2FB", "indigo-400"),
    ("#6875F5", "indigo-500"),
    ("#5850EC", "indigo-600"),
    ("#5145CD", "indigo-700"),
    ("#42389D", "indigo-800"),
    # Purple
    ("#EDEBFE", "purple-100"),
    ("#DCD7FE", "purple-200"),
    ("#CABFFD", "purple-300"),
    ("#AC94FA", "purple-400"),
    ("#9061F9", "purple-500"),
    ("#7E3AF2", "purple-600"),
    ("#6C2BD9", "purple-700"),
    ("#5521B5", "purple-800"),
    # Pink
    ("#FDF2F8", "pink-100"),
    ("#FAD1E8", "pink-200"),
    ("#F8B4D9", "pink-300"),
    ("#F17EB8", "pink-400"),
    ("#E74694", "pink-500"),
    ("#D61F69", "pink-600"),
    ("#BF125D", "pink-700"),
    ("#99154B", "pink-800"),
    # Greens
    ("#7DD181", "Mantis"),
    ("#16DB65", "Malachite"),
    ("#51CB20", "Lime Green"),
    ("#BDD358", "June Bud"),
    ("#68A357", "Asparagus"),
    ("#32965D", "Green Cyan"),
    ("#09814A", "Sea Green"),
    ("#317B22", "Ao English"),
    # Reds
    ("#F1A7A9", "Pastel Pink"),
    ("#EC8385", "Light Coral"),
    ("#E66063", "Fuzzy Wuzzy"),
    ("#E35053", "Indian Red"),
    ("#FF3C38", "Tart Orange"),
    ("#E3170A", "Vermilion"),
    ("#BD1F21", "Firebrick"),
    ("#9C191B", "Ruby Red"),
    ("#F95738", "Orange Soda"),
    ("#D34E24", "Sinopia"),
    ("#EC9A29", "Carrot Orange"),
    ("#FF8C42", "Mango Tango"),
    ("#EE6352", "Fire Opal"),
    ("#F56476", "Fiery Rose"),
    ("#E87461", "Terra Cotta"),
    ("#E5C687", "Gold Crayola"),
    ("#FAC9B8", "Apricot"),
    ("#A1E8CC", "Magic Mint"),
    ("#41E2BA", "Medium Aquamarine"),
    ("#0F8B8D", "Dark Cyan"),
    ("#85C7F2", "Light Sky Blue"),
    ("#A1B5D8", "Wild Blue Yonder"),
    ("#805D93", "French Lilac"),
    ("#6F73D2", "Violet Blue Crayola"),
]


def is_color_dark(hex_color):
    """
    Check if a color in hex format is dark or light.
    """
    hex_color = hex_color.strip("#")
    # Get the RGB values from the hex code.
    red, green, blue = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    # Calculate the luminance of the color using the formula for relative luminance.
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    # Check if the luminance is less than or equal to 50% (i.e., if the color is dark).
    if luminance <= 127:
        return True
    else:
        return False


def get_month_range(start_day_of_month: int, date_to_check: date):
    if start_day_of_month <= date_to_check.day:
        first_day = date(date_to_check.year, date_to_check.month, start_day_of_month)
    else:
        first_day = date(
            date_to_check.year, date_to_check.month, start_day_of_month
        ) - relativedelta(months=1)
    last_day = first_day + relativedelta(months=1) - relativedelta(days=1)
    return first_day, last_day


def hex_to_rgb(hex_string):
    hex_color = hex_string.lstrip("#")
    rgb_string = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f"rgb{rgb_string}"
