**1\. Mục tiêu:** Xây dựng một chương trình giải trò chơi xếp hình 8 ô với giao diện đồ họa sử dụng thư viện Pygame, hỗ trợ các tính năng:

- Cho phép người dùng di chuyển các ô số thủ công trên bảng 3x3 bằng chuột hoặc phím mũi tên.
- Tích hợp nhiều thuật toán tìm kiếm khác nhau để tự động giải bài toán từ trạng thái ban đầu đến trạng thái mục tiêu.
- Cung cấp khả năng tạo trạng thái ngẫu nhiên, xuất đường đi giải pháp ra file, và đo thời gian thực thi của từng thuật toán.

**2\. Nội dung**

**2.1. Các thuật toán Tìm kiếm không có thông tin (BFS, DFS, UCS, IDS)**

**Thành phần chính của bài toán tìm kiếm**: Bài toán xếp hình 8 ô được biểu diễn dưới dạng không gian trạng thái, trong đó:

- - - **Trạng thái**: Một mảng 9 phần tử (từ 0 đến 8), với 0 đại diện cho ô trống.
      - Trạng thái bắt đầu: \[4, 2, 3, 5, 1, 8, 0, 6, 7\].
      - Trạng thái mục tiêu là \[1, 2, 3, 4, 5, 6, 7, 8, 0\].
      - **Hành động**: Di chuyển ô trống lên, xuống, trái, hoặc phải, tạo ra trạng thái mới bằng cách hoán đổi ô trống với ô lân cận.
      - **Không gian trạng thái**: Tập hợp tất cả các trạng thái có thể đạt được từ trạng thái ban đầu thông qua các hành động hợp lệ.
      - **Mục tiêu**: Tìm đường đi từ trạng thái ban đầu đến trạng thái mục tiêu.  
            Các thuật toán không có thông tin không sử dụng heuristic, mà khám phá không gian trạng thái dựa trên chiến lược tìm kiếm (chiều rộng, chiều sâu, hoặc chi phí).
    - **Giải pháp:** Một danh sách các trạng thái, đại diện cho đường đi từ trạng thái ban đầu đến trạng thái mục tiêu. Mỗi trạng thái trong danh sách là kết quả của một bước di chuyển hợp lệ.
- **Nhận xét về hiệu suất**:
  - **BFS**: Đảm bảo đường đi ngắn nhất, nhưng tốn nhiều bộ nhớ. Thời gian chạy thường dưới 1 giây cho bài toán đơn giản, nhưng có thể vượt giới hạn bộ nhớ với bài toán phức tạp.
  - **DFS**: Tiết kiệm bộ nhớ hơn BFS, nhanh (dưới 1 giây) nếu tìm được giải pháp, nhưng không tối ưu và dễ thất bại nếu mục tiêu ở nhánh khác.
  - **UCS**: Tương tự BFS, tối ưu nhưng tốn bộ nhớ, thời gian chạy từ 0.5 đến 2 giây.
  - **IDS**: Kết hợp BFS và DFS, tối ưu và ít tốn bộ nhớ hơn BFS, thời gian chạy 1-3 giây cho bài toán trung bình.

**2.2. Các thuật toán Tìm kiếm có thông tin (Greedy, A\*, IDA\*)**

- - **Thành phần chính**: Bao gồm trạng thái, hành động, không gian trạng thái, và mục tiêu. Các thuật toán có thông tin sử dụng **heuristic** (khoảng cách Manhattan) để định hướng tìm kiếm, giảm số trạng thái cần khám phá.
    - **Giải pháp**: Một danh sách các trạng thái từ trạng thái ban đầu đến trạng thái mục tiêu, thường được tìm nhanh hơn nhờ heuristic, nhưng không phải lúc nào cũng tối ưu (ví dụ: Greedy).
- **Nhận xét**:
  - **Greedy**: Rất nhanh (dưới 0.5 giây), nhưng không tối ưu và dễ thất bại nếu kẹt ở nhánh sai.
  - **A**\*: Tối ưu, nhanh (0.02-0.5 giây), hiệu quả về bộ nhớ và thời gian, phù hợp với hầu hết các bài toán.
  - **IDA**\*: Tiết kiệm bộ nhớ hơn A\*, thời gian chạy 0.5-1 giây, chậm hơn A\* nhưng khả thi với hệ thống hạn chế bộ nhớ.

**2.3. Học củng cố (Q-Learning)**

- - **Thành phần chính của bài toán tìm kiếm**: Q-Learning học chính sách di chuyển qua thử và sai:
        - **Trạng thái**: Cấu hình của bảng 8 ô.
        - **Hành động**: Di chuyển ô trống.
        - **Phần thưởng**: Âm (dựa trên khoảng cách Manhattan), dương (+100) khi đạt mục tiêu.  
            Bảng Q lưu giá trị dự kiến của hành động, được cập nhật qua các vòng lặp.
    - **Giải pháp**: Chuỗi trạng thái từ trạng thái ban đầu đến mục tiêu, được tạo sau khi học chính sách tối ưu.
- **Nhận xét về hiệu suất**:
  - Q-Learning không hiệu quả do bài toán 8 ô là xác định, cần nhiều thời gian học (thường vượt 15 giây) và không hội tụ trong giới hạn thử nghiệm.

**2.4. Tìm kiếm cục bộ (Simple Hill Climbing, Steepest Hill Climbing, Stochastic Hill Climbing, Simulated Annealing, Local Beam Search)**

- - **Thành phần chính**: Sử dụng heuristic (khoảng cách Manhattan) để cải thiện trạng thái hiện tại qua các bước di chuyển ô trống, tập trung vào trạng thái lân cận mà không khám phá toàn bộ không gian.
    - **Giải pháp**: Chuỗi trạng thái dẫn đến mục tiêu, hoặc None nếu kẹt ở cực trị cục bộ.
- **Nhận xét về hiệu suất**:
  - **Simple Hill Climbing**: Nhanh (dưới 0.1 giây), nhưng dễ kẹt ở cực trị cục bộ.
  - **Steepest Hill Climbing**: Tương tự, dưới 0.2 giây, nhưng xác suất thất bại cao.
  - **Stochastic Hill Climbing**: Dưới 0.3 giây, ổn định hơn nhờ ngẫu nhiên, nhưng kết quả không nhất quán.
  - **Simulated Annealing**: Thường không tìm được giải pháp trong 15 giây do tốc độ làm mát chậm.
  - **Local Beam Search**: 0.5-1 giây, hiệu quả hơn Hill Climbing, nhưng vẫn có thể thất bại.

**2.5. Tìm kiếm trong môi trường không xác định (AND-OR Graph Search)**

**Thành phần chính**: Trong môi trường không xác định, hành động di chuyển ô trống có xác suất dẫn đến kết quả không mong muốn (20% khả năng tạo ra một trạng thái ngẫu nhiên hợp lệ thay vì di chuyển đúng hướng).

- **Trạng thái**: Cấu hình bảng 8 ô.
- **Hành động**: Di chuyển ô trống (lên, xuống, trái, phải), với mô hình chuyển tiếp xác suất (80% đúng hành động, 20% ngẫu nhiên).
- **Mục tiêu**: Đạt trạng thái mục tiêu \[1, 2, 3, 4, 5, 6, 7, 8, 0\].
- **Giải pháp**: Một kế hoạch điều kiện (cây hoặc chuỗi trạng thái) đảm bảo đạt mục tiêu bất kể kết quả không xác định.
- **Nhận xét về hiệu suất**:
  - **Thời gian**: 1–5 giây, phụ thuộc vào độ phức tạp của không gian trạng thái và số lượng kết quả không xác định.
  - **Bộ nhớ**: Cao, do cần lưu trữ nhiều kết quả có thể xảy ra cho mỗi hành động.
  - **Tính tối ưu**: Đảm bảo tìm giải pháp nếu tồn tại, nhưng không phải lúc nào cũng là đường đi ngắn nhất do tính không xác định.
  - **Tính ổn định**: Ổn định trong việc tìm giải pháp, nhưng nhạy cảm với xác suất của các di chuyển không mong muốn.

**2.6. Tìm kiếm có ràng buộc (AC3, Backtracking)**

**Thành phần chính**: Bài toán 8 ô được biểu diễn như một bài toán thỏa mãn ràng buộc (CSP):

- **Biến**: 9 vị trí trên bảng 3x3.
- **Miền giá trị**: Mỗi vị trí có thể nhận giá trị {0, 1, 2, 3, 4, 5, 6, 7, 8}, với 0 là ô trống.
- **Ràng buộc**: Mỗi giá trị phải duy nhất (ràng buộc all-different), và cấu hình cuối phải thỏa mãn giá trị {0, 1, 2, 3, 4, 5, 6, 7, 8}.
- **Mục tiêu**: Gán giá trị cho các vị trí để thỏa mãn tất cả ràng buộc và đạt trạng thái mục tiêu.
- **Giải pháp**:
  - **AC3**: Một chuỗi trạng thái (hoặc trạng thái duy nhất) sau khi thực thi tính nhất quán cung, nhưng có thể không tạo ra đường đi đầy đủ.
  - **Backtracking**: Một chuỗi trạng thái đại diện cho các di chuyển hợp lệ từ trạng thái ban đầu đến mục tiêu.
- **Nhận xét về hiệu suất**:
  - **AC3**:
    - **Thời gian**: 0.1–0.5 giây, nhanh trong việc truyền bá ràng buộc nhưng không phải là thuật toán tìm đường hoàn chỉnh.
    - **Bộ nhớ**: Thấp, chỉ lưu trữ miền giá trị và ràng buộc.
    - **Tính tối ưu**: Không áp dụng, vì đây là bước tiền xử lý thay vì tìm đường đi.
    - **Tính ổn định**: Ổn định nhưng không hoàn chỉnh nếu không kết hợp với backtracking.
  - **Backtracking**:
    - **Thời gian**: 0.5–3 giây, phụ thuộc vào độ sâu của tìm kiếm.
    - **Bộ nhớ**: Trung bình, lưu trữ đường đi hiện tại và các gán giá trị tạm thời.
    - **Tính tối ưu**: Có thể tối ưu nếu sử dụng heuristic, nhưng thường khám phá nhiều nhánh.
    - **Tính ổn định**: Ổn định nhưng nhạy cảm với thứ tự gán biến.

**2.7. So sánh các thuật toán**

**Thời gian thực thi**:

- - **Tìm kiếm không thông tin**:
        - BFS: 0.1–1 giây, đảm bảo đường đi ngắn nhất nhưng chậm với trạng thái phức tạp.
        - DFS: <1 giây nếu may mắn, nhưng thường thất bại hoặc vượt quá 10 giây.
        - UCS: 0.5–2 giây, tương tự BFS nhưng xem xét chi phí đồng đều.
        - IDS: 1–3 giây, cân bằng giữa thời gian và bộ nhớ.
    - **Tìm kiếm có thông tin**:
      - Greedy: <0.5 giây, nhanh nhưng không tối ưu.
      - A\*: 0.02–0.5 giây, nhanh nhất và tối ưu trong nhóm có thông tin.
      - IDA\*: 0.5–1 giây, chậm hơn A\* nhưng tiết kiệm bộ nhớ.
    - **Tìm kiếm cục bộ**:
      - Simple Hill Climbing: <0.1 giây, rất nhanh nhưng dễ kẹt.
      - Steepest Hill Climbing: <0.2 giây, tốt hơn một chút nhưng vẫn dễ thất bại.
      - Stochastic Hill Climbing: <0.3 giây, ổn định hơn nhờ ngẫu nhiên nhưng không đồng nhất.
      - Simulated Annealing: 0.5–15 giây, chậm do lịch làm mát.
      - Local Beam Search: 0.5–1 giây, hiệu quả hơn Hill Climbing nhưng không luôn thành công.
    - **Học củng cố**:
      - Q-Learning: >15 giây, không hiệu quả do giai đoạn học kéo dài và bản chất xác định của bài toán.
    - **Tìm kiếm không xác định**:
      - AND-OR Graph Search: 1–5 giây, chậm hơn do khám phá nhiều kết quả có thể xảy ra.
    - **Tìm kiếm có ràng buộc**:
      - AC3: 0.1–0.5 giây, nhanh trong truyền bá ràng buộc nhưng không tạo đường đi đầy đủ.
      - Backtracking: 0.5–3 giây, hợp lý nhưng phụ thuộc vào thứ tự gán biến.
- **Bộ nhớ sử dụng**:
  - **Cao**: BFS, UCS, AND-OR Graph Search (lưu trữ tất cả trạng thái hoặc kết quả).
  - **Trung bình**: A\*, Backtracking, Local Beam Search (lưu trữ đường đi hoặc chùm trạng thái).
  - **Thấp**: DFS, IDS, IDA\*, AC3, các biến thể Hill Climbing, Simulated Annealing (lưu trữ tối thiểu trạng thái).
  - **Biến đổi**: Q-Learning (phụ thuộc vào kích thước bảng Q).
- **Độ tối ưu của giải pháp**:
  - **Tối ưu**: BFS, UCS, IDS, A\* (đường đi ngắn nhất).
  - **Tối ưu có điều kiện**: IDA\*, Backtracking (với heuristic phù hợp).
  - **Không tối ưu**: Greedy, các biến thể Hill Climbing, Simulated Annealing, Local Beam Search, Q-Learning, AND-OR Graph Search, AC3.
- **Tính ổn định**:
  - **Cao**: A\*, BFS, UCS, IDS, AC3 (giới hạn tài nguyên).
  - **Trung bình**: IDA\*, Backtracking, AND-OR Graph Search, Local Beam Search, Simulated Annealing (phụ thuộc vào tham số hoặc ngẫu nhiên).
  - **Thấp**: DFS, Greedy, các biến thể Hill Climbing, Q-Learning, Stochastic Hill Climbing (nhạy cảm với trạng thái ban đầu hoặc yếu tố ngẫu nhiên).

**3\. Kết luận**

Triển khai thành công giao diện đồ họa Pygame, tích hợp 16 thuật toán tìm kiếm thuộc nhiều nhóm (không thông tin, có thông tin, học củng cố, tìm kiếm cục bộ).

- - Tính năng tạo trạng thái ngẫu nhiên, xuất đường đi, và thao tác thủ công hoạt động hiệu quả.
    - A\* và BFS cho kết quả tốt (dưới 1 giây cho bài toán trung bình), trong khi Q-Learning và AC3 không hiệu quả do không phù hợp với đặc điểm 8 ô.
    - Cải thiện: Tối ưu tham số cho các thuật toán ngẫu nhiên và tối ưu hàm heuristic
