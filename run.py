import subprocess
from arb.exchange_config import *
import sys, os
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
import time
from os import name,system
from colorama import Style, Fore, init
init()
def clear():
    if name == 'nt':
      system('cls')
    else:
        system('clear')

current_dir = os.path.dirname(os.path.abspath(__file__))

usable_balance_path = os.path.join(current_dir, "usable_balance.txt")
total_balance_path = os.path.join(current_dir, "total_balance.txt")
fake_money_path = os.path.join(current_dir, "bot-fake-money.py")
bot_path = os.path.join(current_dir, "bot.py")
main_path = os.path.join(current_dir, "main.py")
logs_path = os.path.join(current_dir, "logs/logs.txt")

try:
    if len(sys.argv) < 3:
        input_list = ["mode (fake-money or real)", "renewal period (in minutes)", "balance to use", "symbol", "exchanges list separated without space with commas (,)"]
        if not renewal:
            input_list.remove("renewal period (in minutes)")
        output = []
        
        for inputt in input_list:
            output.append(input(inputt+" >>> "))
        
        mode = output[0]
        if not renewal:
            renew_time = "525600"
            balance=output[1]
            symbol = output[2]
            ex_list = output[3]
        else:
            renew_time = output[1]
            balance=output[2]
            symbol = output[3]
            ex_list = output[4]

        if mode!='fake-money':
            real_balance=0
            with open(usable_balance_path,"w") as f:
                f.write(str(balance))
            for ex_str in ex_list.split(','):
                bal = ex[ex_str].fetchBalance()
                real_balance+=float(bal[symbol.split('/')[1]]['total'])
            with open(total_balance_path,"w") as f:
                f.write(str(real_balance))

        if renewal:
            subprocess.run([python_command,main_path,mode,renew_time,balance,symbol,ex_list])
        else:
            subprocess.run([python_command,main_path,mode,balance,symbol,ex_list])

    else:
        if (len(sys.argv) != 6) and renewal:
            printerror(m=f"Not correctly configured. Usage:\n \n{python_command} run.py <mode> <renewal period minutes> <balance to use> <crypto pair> <exchanges list separated without space with commas (,)>\n")
            sys.exit(1)
        if (len(sys.argv) != 5) and not renewal:
            printerror(m=f"Not correctly configured. Usage:\n \n{python_command} run.py <mode> <balance to use> <crypto pair> <exchanges list separated without space with commas (,)>\n")
            sys.exit(1)
        args = sys.argv
        
        mode = args[1]
        if not renewal:
            renew_time = "525600"
            balance=args[2]
            symbol = args[3]
            ex_list = args[4]
        else:
            renew_time = args[2]
            balance=args[3]
            symbol = args[4]
            ex_list = args[5]

        if mode!='fake-money':
            real_balance=0
            with open(usable_balance_path,"w") as f:
                f.write(str(balance))
            for ex_str in ex_list.split(','):
                bal = ex[ex_str].fetchBalance()
                real_balance+=float(bal[symbol.split('/')[1]]['total'])
            with open(total_balance_path,"w") as f:
                f.write(str(real_balance))
        else:
            with open(total_balance_path,"w") as f:
                f.write(str(balance))
        print('''
                                                                                                                     
                                                                                                                     
 A    RRRR   BBBB  
A A   R   R  B   B 
AAA   RRRR   BBBB  
A A   R  R   B   B  
A A   R   R  BBBB  
                                                                                                                     
                                                                                                                     ''')
        i=0

        while True:
            with open(usable_balance_path,"r") as f:
                balance = str(f.read())
            if i>=1 and 'p' in locals() and p.returncode==1:
                sys.exit(1)
            if mode == "fake-money":
                if os.path.exists(fake_money_path):
                    p=subprocess.run([python_command,fake_money_path,symbol,balance,renew_time,symbol,ex_list])
                else:
                    printerror(m=f'please put the file "bot-fake-money.py" in the current directory.')
            elif mode == "real":
                if os.path.exists(bot_path):
                    p=subprocess.run([python_command,bot_path,symbol,balance,renew_time,symbol,ex_list])
                else:
                    printerror(m=f'please put the file "bot.py" in the current directory.')
            else:
                printerror(m=f"mode input is incorrect.")
                sys.exit(1)
            i+=1
except KeyboardInterrupt:
    if mode!='fake-money':
        print(" \n \n \n")
        clear()
        answered = False
        while answered == False:
            inp = input(f"{get_time()} CTRL+C was pressed. Do you want to sell all crypto back? (y)es / (n)o\n \ninput: ")
            append_new_line(logs_path,f"{get_time_blank()} INFO: ctrl+c was pressed.")
            if inp.lower() == "y" or inp.lower() == "yes":
                answered = True
                emergency_convert_list(symbol,[ex_list.split(',')[i] for i in range(len(ex_list.split(',')))])
                sys.exit(1)
            if inp.lower() == "n" or inp.lower() == "no":
                answered = True
                sys.exit(1)
            else:
                answered = False
    else:
        pass

