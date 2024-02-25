import multiprocessing
import subprocess
from time import sleep
import sys
sys.path.append('API')
sys.path.append('extract1To3')
sys.path.append('extractAddress')
from extract1To3 import extract1_1To3
from extract1To3 import extract1_2To3
from extractAddress import extractAddress_1
from extractAddress import extractAddress_2
import os

def multiRunScript(script_name):
    subprocess.call(["python", script_name])

def main():
    decision = input('Do you want to delete other files? Please input "yes" or "no" : ')
    # Step1. Take SSL from Computer Assisted Mass Appraisal pages such as Residential: https://opendata.dc.gov/datasets/DCGIS::computer-assisted-mass-appraisal-residential/about and Condo: https://opendata.dc.gov/datasets/DCGIS::computer-assisted-mass-appraisal-condominium/about
    # Step2. Save Attributes (See below) in JSON format
    step1_scripts = ["./API/api_step1_1.py", "./API/api_step1_2.py", "./API/api_step3.py", "./API/api_step4.py"]
    step1_processes = []
    for script in step1_scripts:
        step1_process = multiprocessing.Process(target = multiRunScript, args = (script,))
        step1_processes.append(step1_process)
        step1_process.start()
    for step1_process in step1_processes:
        step1_process.join()

    # Step3. Using Address and Suffix Lot Cross Reference Link: (https://opendata.dc.gov/datasets/DCGIS::address-and-square-suffix-lot-cross-reference/about) look up the SSL (4 spaces between the numbers) retriever the Address_ID or MARID (they are the same).
    extract1_1To3.extract1_1To3()
    sleep(2)
    extract1_2To3.extract1_2To3()
    sleep(3)

    # Step4. Using Address Points (https://opendata.dc.gov/datasets/DCGIS::address-points/about) match the Address_ID with the Street Address.  
    extractAddress_1.extractAddress_1()
    sleep(2)
    extractAddress_2.extractAddress_2()
    sleep(3)

    # Step5. Add the Street Address to the JSON.
    step5_scripts = ["./extractAddress/addAddress_1.py", "./extractAddress/addAddress_2.py"]
    step5_processes = []
    for script in step5_scripts:
        step5_process = multiprocessing.Process(target = multiRunScript, args = (script,))
        step5_processes.append(step5_process)
        step5_process.start()
    for step5_process in step5_processes:
        step5_process.join()

    if decision == 'yes':
        # Delete other JSON files.
        file_paths = [
            './output1_1.json',
            './output1_2.json',
            './output3.json',
            './output4.json',
            './match1_1&3.json',
            './match1_2&3.json',
            './addAddress_1.json',
            './addAddress_2.json',
            './extractAddress_1.json',
            './extractAddress_2.json',
            ]

        for file_path in file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File {file_path} has been removed.")
            else:
                print('Failed run script.')

if __name__ == '__main__':
    main()