import pymysql
import getpass

MYSQL_PASSWORD = getpass.getpass("Enter MySQL password: ")

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password=MYSQL_PASSWORD,
        database="book_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# ========== READ OPERATIONS ==========

def list_all_books():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('get_all_book_detail')
            results = cursor.fetchall()
            if results:
                print("\n" + "="*80)
                print("ALL BOOKS")
                print("="*80)
                for row in results:
                    print(f"ID: {row['book_id']} | {row['title']} ({row['englishtitle']})")
                    print(f"   Genre: {row['genre']} | Status: {row['status']} | Author: {row['author']}")
                    print("-"*80)
            else:
                print("No books found.")
    finally:
        conn.close()

def get_book_detail():
    book_id = input("Enter book ID: ").strip()
    if not book_id.isdigit():
        print("Invalid book ID\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('get_book_detail', (int(book_id),))
            result = cursor.fetchone()
            if result:
                print("\n" + "="*80)
                print(f"Book ID: {result['book_id']}")
                print(f"Title: {result['title']}")
                print(f"English Title: {result['englishtitle']}")
                print(f"Genre: {result['genre']}")
                print(f"Status: {result['status']}")
                print(f"Author: {result['author']}")
                print("="*80 + "\n")
            else:
                print("Book not found.\n")
    finally:
        conn.close()

def search_books():
    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        print("Keyword cannot be empty\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('search_books', (keyword,))
            results = cursor.fetchall()
            if results:
                print("\n" + "="*80)
                print(f"SEARCH RESULTS FOR: {keyword}")
                print("="*80)
                for row in results:
                    print(f"ID: {row['book_id']} | {row['title']} ({row['englishtitle']})")
                    print(f"   Genre: {row['genre']} | Status: {row['status']} | Author: {row['authors']}")
                    print("-"*80)
            else:
                print(f"No books found matching '{keyword}'.\n")
    finally:
        conn.close()

def search_books_by_author():
    author = input("Enter author name: ").strip()
    if not author:
        print("Author name cannot be empty\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('search_books_by_author', (author,))
            results = cursor.fetchall()
            if results:
                print("\n" + "="*80)
                print(f"BOOKS BY: {author}")
                print("="*80)
                for row in results:
                    print(f"ID: {row['book_id']} | {row['title']} ({row['englishtitle']})")
                    print(f"   Genre: {row['genre']} | Status: {row['status']}")
                    print("-"*80)
            else:
                print(f"No books found by author '{author}'.\n")
    finally:
        conn.close()

def list_all_reviews():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('get_all_review')
            results = cursor.fetchall()
            if results:
                print("\n" + "="*80)
                print("ALL REVIEWS")
                print("="*80)
                for row in results:
                    print(f"Book: {row['title']} ({row['englishtitle']})")
                    print(f"Review #{row['review_number']} | Rating: {row['rating']}/5")
                    print(f"Notes: {row['notes']}")
                    print("-"*80)
            else:
                print("No reviews found.")
    finally:
        conn.close()

def get_reviews_by_book():
    book_id = input("Enter book ID: ").strip()
    if not book_id.isdigit():
        print("Invalid book ID\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('get_review_detail_by_bookid', (int(book_id),))
            results = cursor.fetchall()
            if results:
                print("\n" + "="*80)
                print(f"REVIEWS FOR: {results[0]['title']}")
                print("="*80)
                for row in results:
                    print(f"Review #{row['review_number']} | Rating: {row['rating']}/5")
                    print(f"Notes: {row['notes']}")
                    print("-"*80)
            else:
                print("No reviews found for this book.\n")
    finally:
        conn.close()

# ========== CREATE OPERATIONS ==========

def add_book_by_id():
    print("\n--- Add Book (using IDs) ---")
    title = input("Title: ").strip()
    englishtitle = input("English title: ").strip()
    genre_id = input("Genre ID: ").strip()
    status_id = input("Status ID: ").strip()
    author_name = input("Author name: ").strip()
    
    if not all([title, englishtitle, genre_id, status_id, author_name]):
        print("All fields are required\n")
        return
    
    if not genre_id.isdigit() or not status_id.isdigit():
        print("Genre ID and Status ID must be numbers\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('add_book', (title, englishtitle, int(genre_id), int(status_id), author_name))
            conn.commit()
            print("Book added successfully!\n")
    except pymysql.Error as e:
        print(f"Error: {e}\n")
        conn.rollback()
    finally:
        conn.close()

def add_book_by_names():
    print("\n--- Add Book (using names) ---")
    title = input("Title: ").strip()
    englishtitle = input("English title: ").strip()
    genre_name = input("Genre name: ").strip()
    status_name = input("Status name: ").strip()
    author_name = input("Author name: ").strip()
    
    if not all([title, englishtitle, genre_name, status_name, author_name]):
        print("All fields are required\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('add_book_by_names', (title, englishtitle, genre_name, status_name, author_name))
            conn.commit()
            print("Book added successfully!\n")
    except pymysql.Error as e:
        print(f"Error: {e}\n")
        conn.rollback()
    finally:
        conn.close()

def add_review():
    print("\n--- Add Review ---")
    book_id = input("Book ID: ").strip()
    rating = input("Rating (1-5): ").strip()
    notes = input("Notes: ").strip()
    
    if not book_id.isdigit() or not rating.isdigit():
        print("Book ID and Rating must be numbers\n")
        return
    
    rating_val = int(rating)
    if rating_val < 1 or rating_val > 5:
        print("Rating must be between 1 and 5\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('add_review', (int(book_id), rating_val, notes))
            conn.commit()
            print("Review added successfully!\n")
    except pymysql.Error as e:
        print(f"Error: {e}\n")
        conn.rollback()
    finally:
        conn.close()

# ========== UPDATE OPERATIONS ==========

def update_book_status():
    print("\n--- Update Book Status ---")
    book_id = input("Book ID: ").strip()
    status_id = input("New Status ID: ").strip()
    
    if not book_id.isdigit() or not status_id.isdigit():
        print("Book ID and Status ID must be numbers\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('update_book_status', (int(book_id), int(status_id)))
            conn.commit()
            print("Book status updated successfully!\n")
    except pymysql.Error as e:
        print(f"Error: {e}\n")
        conn.rollback()
    finally:
        conn.close()

# ========== DELETE OPERATIONS ==========

def delete_book():
    print("\n--- Delete Book ---")
    book_id = input("Book ID to delete: ").strip()
    
    if not book_id.isdigit():
        print("Book ID must be a number\n")
        return
    
    confirm = input(f"Are you sure you want to delete book {book_id}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Delete cancelled.\n")
        return
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('delete_book', (int(book_id),))
            conn.commit()
            print("Book deleted successfully!\n")
    except pymysql.Error as e:
        print(f"Error: {e}\n")
        conn.rollback()
    finally:
        conn.close()

# ========== HELPER FUNCTIONS ==========

def list_genres():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT genre_id, name FROM genre ORDER BY genre_id")
            results = cursor.fetchall()
            print("\n[GENRES]")
            for row in results:
                print(f"  {row['genre_id']}: {row['name']}")
            print()
    finally:
        conn.close()

def list_statuses():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT status_id, name FROM read_status ORDER BY status_id")
            results = cursor.fetchall()
            print("\n[READ STATUSES]")
            for row in results:
                print(f"  {row['status_id']}: {row['name']}")
            print()
    finally:
        conn.close()

def list_authors():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT author_id, name FROM author ORDER BY author_id")
            results = cursor.fetchall()
            print("\n[AUTHORS]")
            for row in results:
                print(f"  {row['author_id']}: {row['name']}")
            print()
    finally:
        conn.close()

# ========== MAIN MENU ==========

def main():
    while True:
        print("\n" + "="*50)
        print("BOOK DATABASE - MAIN MENU")
        print("="*50)
        print("\n--- READ Operations ---")
        print("1)  List all books")
        print("2)  Get book details")
        print("3)  Search books by keyword")
        print("4)  Search books by author")
        print("5)  List all reviews")
        print("6)  Get reviews for a book")
        print("\n--- CREATE Operations ---")
        print("7)  Add a book (using genre/status IDs)")
        print("8)  Add a book (using genre/status names)")
        print("9)  Add a review")
        print("\n--- UPDATE Operations ---")
        print("10) Update book status")
        print("\n--- DELETE Operations ---")
        print("11) Delete a book")
        print("\n--- Reference Lists ---")
        print("12) Show all genres")
        print("13) Show all statuses")
        print("14) Show all authors")
        print("\n0)  Exit")
        print("="*50)
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            list_all_books()
        elif choice == "2":
            get_book_detail()
        elif choice == "3":
            search_books()
        elif choice == "4":
            search_books_by_author()
        elif choice == "5":
            list_all_reviews()
        elif choice == "6":
            get_reviews_by_book()
        elif choice == "7":
            add_book_by_id()
        elif choice == "8":
            add_book_by_names()
        elif choice == "9":
            add_review()
        elif choice == "10":
            update_book_status()
        elif choice == "11":
            delete_book()
        elif choice == "12":
            list_genres()
        elif choice == "13":
            list_statuses()
        elif choice == "14":
            list_authors()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
