# test_cloudpref.py
from cloudpref_metr import CloudPrefMETR

def main():
    evaluator = CloudPrefMETR()
    task = evaluator.generate_task()
    print("Generated Task:")
    print(task)

    # You can add more tests or usage examples here

if __name__ == "__main__":
    main()