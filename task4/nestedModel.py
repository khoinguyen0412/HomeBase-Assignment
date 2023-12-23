import sqlite3

# Function to insert a node into the nested set model
def insert_node(name, parent_id=None):
    if parent_id is None:
        # Insert as root node
        cursor.execute(
            "INSERT INTO nested_set (name, lft, rgt) VALUES(?, 1 , 2)", (name,))
    else:
        # Insert as child node
        cursor.execute("SELECT rgt FROM nested_set WHERE id = ?", (parent_id,))
        parent_rgt = cursor.fetchone()[0]

        cursor.execute("UPDATE nested_set SET rgt = rgt + 2 WHERE rgt > ?", (parent_rgt,))
        cursor.execute("UPDATE nested_set SET lft = lft + 2 WHERE lft > ?", (parent_rgt,))

        cursor.execute("INSERT INTO nested_set (name, lft, rgt) VALUES (?, ?, ?)", (name, parent_rgt, parent_rgt + 1))
        
        # Update the parent node's right value
        cursor.execute('''
            UPDATE nested_set
            SET rgt = rgt + 2
            WHERE id = ?
        ''', (parent_id,))

        conn.execute("COMMIT")

# Function to retrieve the tree structure
def get_tree_structure():
    cursor.execute('''
        SELECT id, name, lft, rgt FROM nested_set
        ORDER BY lft
    ''')
    return cursor.fetchall()


if __name__ == '__main__':
    conn = sqlite3.connect('./task4/nested_model.db')
    cursor = conn.cursor()

    # Create a table for the nested set model
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nested_set (
            id INTEGER PRIMARY KEY,
            name TEXT,
            lft INTEGER,
            rgt INTEGER
        )
    ''')

# Insert nodes into the nested set model
    insert_node('Root')
    insert_node('Node 1', parent_id=1)
    insert_node('Node 2', parent_id=1)
    insert_node('Node 1.1', parent_id=2)
    insert_node('Node 1.2', parent_id=2)

    # Display the tree structure
    tree_structure = get_tree_structure()
    for node in tree_structure:
        print(f'Node {node[0]}: {node[1]} (left: {node[2]}, right: {node[3]})')

    # Close the database connection
    conn.close()


# With proper indexing, this would improve the performance of the program
# In a large dataset, when inserting a child node, it would take more time 
# if there are many elements to the right side of the new node
#  Minimize the use of subqueries where possible becasue they are resource-intensive
