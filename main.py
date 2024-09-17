
class Call():

    def call_me(self,number):
        print(f"Calling {number}")

class Callme(Call):

    def call_me(self,number):
        super().call_me(number)
        print(f"Calling {number} from subclass")

def main():
    c = Callme()
    c.call_me(1234)
    pass

main()
print("end")