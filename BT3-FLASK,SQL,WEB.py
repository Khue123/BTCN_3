from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras  # Thư viện giúp làm việc với PostgreSQL, đặc biệt là sử dụng DictCursor

app = Flask(__name__)  # Khởi tạo ứng dụng Flask
app.secret_key = "cairocoders-ednalan"  # Khóa bí mật dùng để bảo mật session và flash messages

# Thông tin kết nối với cơ sở dữ liệu PostgreSQL
DB_HOST = "localhost"
DB_NAME = "musiccollection"
DB_USER = "postgres"
DB_PASS = "12345"

# Thiết lập kết nối tới cơ sở dữ liệu
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

# Route hiển thị trang chủ với danh sách các bài hát
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  # Tạo cursor để thực hiện truy vấn
    s = "SELECT * FROM music"  # Truy vấn lấy tất cả bài hát từ bảng "music"
    cur.execute(s)  # Thực thi truy vấn SQL
    music_list = cur.fetchall()  # Lấy tất cả các bản ghi từ kết quả truy vấn
    return render_template('index.html', music_list=music_list)  # Trả về template với dữ liệu danh sách bài hát

# Route thêm bài hát mới vào cơ sở dữ liệu
@app.route('/add_song', methods=['POST'])
def add_song():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':  # Kiểm tra phương thức POST
        title = request.form['title']  # Lấy giá trị từ form
        artist = request.form['artist']
        genre = request.form['genre']
        spotify_id = request.form['spotify_id']
        # Thực hiện truy vấn SQL để thêm bài hát vào cơ sở dữ liệu
        cur.execute("INSERT INTO music (title, artist, genre, spotify_id) VALUES (%s, %s, %s, %s)", (title, artist, genre, spotify_id))
        conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        flash('Song Added Successfully')  # Thông báo thành công cho người dùng
        return redirect(url_for('Index'))  # Quay lại trang chủ

# Route chỉnh sửa thông tin bài hát
@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_song(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM music WHERE id = %s', (id,))  # Truy vấn bài hát theo ID
    data = cur.fetchall()  # Lấy dữ liệu bài hát
    cur.close()  # Đóng cursor
    return render_template('edit.html', song=data[0])  # Trả về trang chỉnh sửa với dữ liệu bài hát

# Route cập nhật thông tin bài hát sau khi chỉnh sửa
@app.route('/update/<id>', methods=['POST'])
def update_song(id):
    if request.method == 'POST':  # Kiểm tra phương thức POST
        title = request.form['title']  # Lấy thông tin từ form
        artist = request.form['artist']
        genre = request.form['genre']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Thực hiện truy vấn SQL để cập nhật thông tin bài hát
        cur.execute("""
            UPDATE music
            SET title = %s,
                artist = %s,
                genre = %s
            WHERE id = %s
        """, (title, artist, genre, id))
        conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        flash('Song Updated Successfully')  # Thông báo thành công cho người dùng
        return redirect(url_for('Index'))  # Quay lại trang chủ

# Route xóa bài hát
@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_song(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM music WHERE id = %s', (id,))  # Thực hiện xóa bài hát theo ID
    conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
    flash('Song Removed Successfully')  # Thông báo thành công cho người dùng
    return redirect(url_for('Index'))  # Quay lại trang chủ

# Chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(debug=True)
