def format_number_value(number, precision: int = 3):
        factor = 10 ** precision
        truncated_number = int(number * factor) / factor
        formatted_number = "{:.{}f}".format(truncated_number, precision).rstrip('0').rstrip('.')
        return formatted_number if number % 1 != 0 else int(number)