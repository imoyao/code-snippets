# -*- coding: utf-8 -*-

# 四年一闰；百年不闰,四百年再闰。


# 普通年能被4整除且不能被100整除的为闰年
# 世纪年能被400整除的是闰年。(如2000年是闰年，1900年不是闰年)

class IntError(Exception):
    """自定义一个异常int类"""

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value


class InputError(Exception):
    """自定义一个异常input类"""

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value


def check_input(intnum):
    if not intnum.isdigit():
        raise InputError(intnum)
    elif not isinstance(int(intnum), int):
        raise IntError(intnum)


def main():
    input_str = input("please enter a valid date(2017-06-04): ")
    for temp in input_str.split('-'):
        print(temp)
        try:
            check_input(temp)
        except InputError as foo:
            print("Input err,{} is not a valid input.".format(foo.value))
        except IntError as bar:
            print("int err!pls check the num {}.".format(bar.value))
        except Exception as e:
            raise e


if __name__ == '__main__':
    main()
# else:
# 	return (year, mon, day)

# try:
# 	year = raw_input("please enter an integer for year: ")
# 	check_input(year)
# 	mon = raw_input("please enter an integer for month:")
# 	check_input(mon)
# 	day = raw_input("please enter an integer for day:")
# 	check_input(day)
# except InputError, foo:
# 	print "Input err,{} is not a valid input.".format(foo.value)
# except IntError, foo:
# 	print "int err!pls check the num {}.".format(foo.value)
# except Exception as e:
# 	raise e
