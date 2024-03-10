import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(name="VedicAstro-LLM")
    parser.add_argument("-l", "--loc", type=str, help="Location")
    parser.add_argument("-t", "--dob", type=str, help="Birth Datetime (fmt: '%d-%m-%Y %H:%M')")
    args = parser.parse_args()
