## Bài tập xử lý tiếng nói - nhận diện khẩu lệnh bằng DTW và HMM
1. DTW xây dựng template trung bình từ 3 mẫu cho mỗi khẩu lệnh, tổng là 24 mẫu. Sau đó so khớp từng mẫu cần nhận diện với template trung bình. Thử trên 6000 mẫu âm thanh (toàn bộ tập dữ liệu để huấn luyện HMM) đạt được độ chính xác khoảng 17.20%, tức 1032 mẫu. Các khẩu lệnh phức tạp hơn về âm như **xuống**, **phải** và **nhảy** nhận diện sai khá nhiều.
2. HMM sử dụng 6000 mẫu âm thanh chia ra làm 2 phần: 5900 mẫu để huấn luyện và 100 mẫu để đánh giá. Độ chính xác đạt được khoảng 83%.
3. Video: https://youtu.be/xm7mB2EnA_k