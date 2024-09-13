from decode_request_OK import decode_saml_request
from decode_response import decode_saml_response
from replace_content_OK import replace_content_saml
from pyperclip import copy


def main():
    print("="*60)
    print("SAML TOOLS".center(60))
    print("="*60)
    print("1. Decode SAML request")
    print("2. Decode SAML response")
    print("3. Replace content in SAML response")
    choice = input("Choose an option : ")

#-----------------------------------------------------------------
#----------------------Decode SAML request------------------------
#-----------------------------------------------------------------
    if choice == '1':
        try:
            copy(decode_saml_request())
        except Exception as e:
            print(f"Error decoding SAML request: {e}")
#-----------------------------------------------------------------
#----------------------Decode SAML response-----------------------
#-----------------------------------------------------------------
    elif choice == '2':
        try:
            copy(decode_saml_response())
        except Exception as e:
            print(f"Error decoding SAML response: {e}")

#-----------------------------------------------------------------
#---------------Replace SAML response content---------------------
#-----------------------------------------------------------------
    elif choice == '3':
        try:
            copy(replace_content_saml())
        except Exception as e:
            print(f"Error decoding SAML response: {e}")


    else:
        print("Incorrect choice")




#------------------------------------
#------------------------------------
#------------------------------------
if __name__ == "__main__":
    main()