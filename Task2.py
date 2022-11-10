def split_including_splitter(string, splitters):
    result = []
    left = ''
    for char in string:
        if char in splitters:
            result.append(left)
            result.append(char)
            left = ''
        else:
            left += char
    result.append(left)
    if len(result) > 1:
        return result
    return result[0]


def is_expression(string):
    status = 'begin'
    open_brackets = 0
    signs = ['+', '-', '/', '*']
    for char in string:
        if status == 'begin':
            if char.isdigit():
                status = 'num'
            elif char == '-':
                status = 'after sign'
            elif char == '(':
                open_brackets += 1
            else:
                status = 'error'
                break
        elif status == 'num':
            if char.isdigit():
                continue
            if char == ')':
                open_brackets -= 1
                if open_brackets < 0:
                    status = 'error'
                    break
                status = 'after bracket close'
            elif char in signs:
                status = 'after sign'
            else:
                status = 'error'
                break
        elif status == 'after sign':
            if char == '(':
                status = 'begin'
                open_brackets += 1
            elif char.isdigit():
                status = 'num'
            else:
                status = 'error'
                break
        elif status == 'after bracket close':
            if char in signs:
                status = 'after sign'
            elif char == ')':
                open_brackets -= 1
                if open_brackets < 0:
                    status = 'error'
                    break
            else:
                status = 'error'
                break
    return status != 'error' and open_brackets == 0


def is_int_or_float(string: str):
    if string.isdigit():
        return True
    try:
        float(string)
        return True
    except ValueError:
        return False


def multiply_or_divide(string):
    if '*' not in string and '/' not in string:
        return string
    string = (split_including_splitter(string, ['*', '/']))
    result = 1
    sign = '*'
    for element in string:
        if is_int_or_float(element):
            if sign == '*':
                result *= float(element)
            else:
                result /= float(element)
        elif element:
            sign = element
    return result


def calculate(expression):
    sum_parts = split_including_splitter(expression, ['+', '-'])
    if isinstance(sum_parts, str):
        return multiply_or_divide(sum_parts)
    for i in range(len(sum_parts)):
        sum_parts[i] = multiply_or_divide(sum_parts[i])
    res = 0
    sign = '+'
    for element in sum_parts:
        if isinstance(element, int) or isinstance(element, float):
            if sign == '+':
                res += element
            else:
                res -= element
        elif is_int_or_float(element):
            if sign == '+':
                res += float(element)
            else:
                res -= float(element)
        elif element == '+':
            sign = '+'
        else:
            sign = '-'
    return res


def calculate_with_brackets(string: str):
    current = ''
    while '(' in string:
        for char in string:
            if char == ')':
                equivalent = calculate(current)
                string = string.replace('(' + current + ')', str(equivalent))
                break
            elif char == '(':
                current = ''
            else:
                current += char
    return calculate(string)


def main():
    expression = input('Введите выражение, значение которого хотите посчитать: ').replace(' ', '')
    if is_expression(expression):
        result = calculate_with_brackets(expression)
        print(f'{expression} -> {result}')
    else:
        print('Полученная строка либо не является вычисляемым выражением, либо неправильно оформлена.')


if __name__ == '__main__':
    main()
