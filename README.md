# jiujiuchuan
for web www.jiujiuchuan.com

## database design

    user (username, password, email, view_count, signature) # passwd encoding leverage Bcrypt
    post (id, type, parent_id (fk), title, tags, content_localtion,
     content_header, author_username(fk), post_time, last_modify_time, view_count)
    post_stat ()
    tag (tag_name, post_id (fk))
    private_message (id, type, from_username (fk), to_username (fk), content)



