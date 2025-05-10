#  Treasure Hunt - AI Maze Game

##  Mục tiêu dự án
Dự án xây dựng một trò chơi mê cung (maze game) trong đó **quái vật** sẽ áp dụng các **thuật toán tìm kiếm AI** để đuổi theo người chơi. Mục tiêu chính là:
- Áp dụng các thuật toán tìm kiếm cổ điển và hiện đại của môn học Trí Tuệ Nhân Tạo, để điều khiển hành vi của quái vật một cách thông minh trong môi trường mê cung. 
- Minh họa sự khác nhau giữa các chiến lược tìm kiếm trong một môi trường tương tác.
- Tăng cường trải nghiệm học tập thông qua trò chơi.

## Giới thiệu hệ thống trò chơi
- Người chơi điều khiển nhân vật tìm kho báu trong mê cung.
- Quái vật trong game sẽ tự động tìm đường đến vị trí người chơi dựa trên thuật toán được chọn.
- Giao diện có các chức năng: lựa chọn độ khó, chọn thuật toán, hiển thị đường đi, đặt lại trò chơi, thoát game.
- Có hiệu ứng âm thanh, đồ họa, và hiển thị thông tin số bước đi, thời gian, tọa độ vị trí các nhân vật trong trò chơi.

##  Các thuật toán tìm kiếm đã sử dụng

| Thuật toán | Mô tả |
|-----------|-------|
| **BFS (Breadth-First Search)** |Tìm đường đi ngắn nhất, đơn giản, dễ cài đặt |
| **UCS (Uniform Cost Search)** |Tối ưu với chi phí không đồng đều |
| **A\*** | Kết hợp giữa chi phí thực tế và ước lượng (heuristic), rất tối ưu cho tìm đường. |
| **Beam Search** | Giống A*, nhưng chỉ xét giới hạn số node tốt nhất trong mỗi bước. |
| **Simulated Annealing** | Thuật toán tìm kiếm ngẫu nhiên có khả năng thoát khỏi cực tiểu cục bộ. |
| **Stochastic Hill Climbing** | Leo dốc ngẫu nhiên, dễ rơi vào cực trị cục bộ nhưng nhanh. |
| **Q-Learning** | Thuật toán học tăng cường, quái vật học cách tối ưu đường đi qua trải nghiệm. |
## Cấu trúc Dự án
- `/Image`: Chứa các file hình ảnh được sử dụng trong game.
- `/Maze`: Chứa các file định nghĩa mê cung (maze) cho game.
- `/Sound`: Chứa các file âm thanh sử dụng trong game.
- `/AI.py`: File chứa logic AI, triển khai các thuật toán tìm kiếm (BFS, DFS, A*,...) cho quái vật.
- `/Boat.py`: File quản lý đối tượng "Boat" (có thể là một thực thể trong game).
- `/Colors.py`: File định nghĩa các màu sắc sử dụng trong game.
- `/Config.py`: File cấu hình các thông số game 
- `/Difficulty.txt`: File chứa thông tin về độ khó của game (có thể là các cấp độ khó).
- `/Game.py`: File chứa logic chính của game, điều khiển luồng chơi.
- `/Home.py`: File quản lý giao diện màn hình chính (Home screen).
- `/Key.py`: File xử lý các phím điều khiển trong game.
- `/Main.py`: File chính để chạy game.
- `/Maze.py`: File xử lý logic tạo và quản lý mê cung.
- `/Player.py`: File quản lý đối tượng người chơi (Player).
- `/README.md`: File tài liệu mô tả dự án (file hiện tại).
- `/UI.py`: File xử lý giao diện người dùng (UI) của game.
##  Hướng phát triển
- Mở rộng thêm các thuật toán tìm kiếm nâng cao như Genetic Algorithm, IDA*, hoặc các thuật toán học tăng cường (Reinforcement Learning),hoặc tìm kiếm trong môi trường phức tạp (Complex Environments)
- Bổ sung chức năng cho phép người dùng tự tạo bản đồ mê cung hoặc sinh bản đồ ngẫu nhiên
- Phát triển chế độ nhiều người chơi để tăng tính tương tác và tích hợp hệ thống chấm điểm cũng như bảng xếp hạng để tạo động lực cho người chơi.
- Tối ưu hóa thuật toán cho môi trường phức tạp và mê cung lớn hơn.
##  Thành viên nhóm
- [Nguyễn Thị Phương Thanh] 
- [Lê Hồ Chí Bảo]
- [Dương Quỳnh Như]

---

 *Dự án mang tính học thuật cao, mô phỏng hệ thống trò chơi AI vào môi trường tương tác để nâng cao hiểu biết về thuật toán tìm kiếm.*

