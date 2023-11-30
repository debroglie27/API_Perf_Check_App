from colorama import Fore, Style

def print_performance(code):
    if code == "1":
        print(f"{Fore.LIGHTBLACK_EX}{Style.BRIGHT}.{Style.RESET_ALL}",end='')
    elif code == "2":
        print(f"{Fore.RED}{Style.BRIGHT}-{Style.RESET_ALL}",end='')
    elif code == "3":
        print(f"{Fore.GREEN}{Style.BRIGHT}+{Style.RESET_ALL}",end='')
    elif code == "4":
        print(f"{Fore.LIGHTBLACK_EX}{Style.BRIGHT}={Style.RESET_ALL}",end='')

print_performance("1")
print_performance("2")
print_performance("3")
print_performance("4")