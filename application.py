from database import create_tables, add_keyword, get_keywords, delete_keyword, get_search_history
from main import main as run_analysis

def show_menu():

    print("\n===== AI Daily Report =====")
    print("1. Add Keyword")
    print("2. View Keywords")
    print("3. Delete Keyword")
    print("4. Run Analysis")
    print("5. View History")
    print("6. Exit")

def main():

    create_tables()

    while True:

        show_menu()

        choice = input("\nChoose an option: ")


        if choice == "1":
            while True:

                keyword = input("Enter keyword (press q to quit): ").strip().lower()
                if keyword == "q":
                    break

                add_keyword(keyword)
                print("Added: " + keyword)



        elif choice == "2":

            keywords = get_keywords()

            print("\nCurrent Keywords:")

            for keyword in keywords:
                print("-", keyword)



        elif choice == "3":

            keyword = input(
                "Keyword to delete: "
            ).strip().lower()

            delete_keyword(keyword)

            print("Deleted: " + keyword)



        elif choice == "4":

            print("\nRunning Analysis...")
            print("\nPlease Wait...\n")

            run_analysis()



        elif choice == "5":

            keyword = input("Enter keyword to view history: ").strip().lower()

            history = get_search_history(keyword)

            print("\nSearch History:")

            for row in history:
                run_time = row[0]
                article_count = row[1]
                sentiment = row[2]

                first_line = sentiment.split("\n")[0]
                print(run_time + " | " + "we found: " + str(article_count) + " article(s) | " + first_line)



        elif choice == "6":

            print("Goodbye.")
            break

        else:

            print("Invalid option.")


if __name__ == "__main__":
    main()