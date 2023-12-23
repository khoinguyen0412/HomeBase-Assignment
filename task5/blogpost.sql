-- Create a stored procedure for managing blog posts
DELIMITER //

CREATE PROCEDURE ManageBlogPost(
    IN p_PostID INT,
    IN p_Title VARCHAR(255),
    IN p_Content TEXT,
    IN p_UserID INT,
    IN p_Action VARCHAR(20)
)
BEGIN
    -- Variables for comments
    DECLARE p_CommentID INT;
    DECLARE p_CommentContent TEXT;

    -- Check the action to perform
    CASE p_Action
        WHEN 'AddPost' THEN
            -- Add a new blog post
            INSERT INTO BlogPosts (Title, Content, UserID, CreatedAt)
            VALUES (p_Title, p_Content, p_UserID, NOW());

        WHEN 'GetPostDetails' THEN
            -- Retrieve details of a specific blog post
            SELECT * FROM BlogPosts WHERE PostID = p_PostID;

        WHEN 'UpdatePost' THEN
            -- Update an existing blog post
            UPDATE BlogPosts
            SET Title = p_Title, Content = p_Content
            WHERE PostID = p_PostID;

        WHEN 'DeletePost' THEN
            -- Delete a blog post and its associated comments
            DELETE FROM BlogComments WHERE PostID = p_PostID;
            DELETE FROM BlogPosts WHERE PostID = p_PostID;

        WHEN 'AddComment' THEN
            -- Add a new comment to a blog post
            INSERT INTO BlogComments (PostID, UserID, CommentContent, CreatedAt)
            VALUES (p_PostID, p_UserID, p_CommentContent, NOW());

        WHEN 'DeleteComment' THEN
            -- Delete a comment from a blog post
            DELETE FROM BlogComments WHERE CommentID = p_CommentID;

        WHEN 'GetPostWithComments' THEN
            -- Retrieve a blog post with its comments
            SELECT
                p.PostID,
                p.Title,
                p.Content,
                p.UserID AS PostUserID,
                p.CreatedAt AS PostCreatedAt,
                c.CommentID,
                c.UserID AS CommentUserID,
                c.CommentContent,
                c.CreatedAt AS CommentCreatedAt
            FROM
                BlogPosts p
            LEFT JOIN
                BlogComments c ON p.PostID = c.PostID
            WHERE
                p.PostID = p_PostID;
    END CASE;
END //

DELIMITER ;
