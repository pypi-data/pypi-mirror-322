##  Thư viện Media.

### Cài đặt:

```bash
 $ pip3 install mobio-media-sdk
 ```

#### Log:

- Version: 0.1.1: Thêm mobio token.
- Version: 0.1.2: Add json.dums by func finish_save_file_by_filepath
- Version: 0.1.3: Add func get_path_by_url, get_binary_by_url
    + Hướng dẫn sử dụng:
        + func get_path_by_url -> kết quả trả về là path của url.
          ```python3
          from mobio.sdks.media.mobio_media_sdk import MobioMediaSDK
          MobioMediaSDK().get_path_by_url(url)
          ```
        + func get_binary_by_url -> kết quả trả về là binary của url
          ```python3
          from mobio.sdks.media.mobio_media_sdk import MobioMediaSDK
          MobioMediaSDK().get_binary_by_url(url)
          ```
- Version: 0.1.4: Add func get_filename_by_url
  + Hướng dẫn sử dụng:
    + func get_filename_by_url -> kết quả trả về là filename của url
      ```python3
      from mobio.sdks.media.mobio_media_sdk import MobioMediaSDK
      MobioMediaSDK().get_filename_by_url(url)
      ```
- Version: 0.1.5: Delete system_config
- Version: 0.1.6: Rename get_local_path_by_url -> get_path_by_url
- Version: 0.1.7: Option read file "r" -> "rb"
- Version: 0.1.8: Update lại token call từ Admin
- Version: 0.1.9: Bổ sung tính năng:
  - Tạo public link khi chưa có file upload.
      ```python3
      from mobio.sdks.media.mobio_media_sdk import MobioMediaSDK
      MobioMediaSDK().create_public_url_without_file(
            merchant_id="merchant_id",
            filename="filename",
            mimetype_str="mimetype_str"
      )

      result = {
        'url': '',
        'local_path': '',
        'filename': ''
      }
      ```
      Sau khi xử lý nghiệp vụ xong có thể dùng func sau để Lưu file được lấy path từ URL
      ```python3
       from mobio.sdks.media.mobio_media_sdk import MobioMediaSDK
       MobioMediaSDK().finish_save_file_by_public_url(filepath="filepath", url="url")
      ```
  - Thêm option **file_byte** khi upload file. Option này phục vụ cho nhu cầu upload file bằng bytes.

- Version: 0.2.0: Bổ sung option display, group_ids
- Version: 0.2.1: Bổ sung merchant_id
- Version: 0.2.2: Sửa từ get public-host từ module media sang module Admin.
- Version: 0.2.2 và 0.2.3: Bổ sung phần tính dung lượng file khi trả về.
- Version: 0.2.5: Chuyển việc lấy public-host sang admin-sdk
- Version: 0.2.6: Apply libs m-kafka-sdk-v2
- Version: 0.2.7: Bỏ m-kafka-sdk
- Version: 0.2.8: Fix lỗi encode url với những tên file đặc biệt
- Version: 0.2.9: Nâng cấp confluent_kafka
- Version: 0.2.10: Thêm get mimetype file_byte
- Version: 0.2.11, 0.2.12: Bổ sung thêm tính năng lưu file định dạng byte
- Version: 0.2.13: Bổ sung thêm phần validate định dạng file upload qua SDK. Nếu không truyền lên thì sẽ lấy mặc định của hệ thống.
    - Hướng dẫn sử dụng
    ```python3
      from mobio.sdks.media.mobio_media_sdk import MobioMediaSDK
      MobioMediaSDK().upload_without_kafka(
          merchant_id="",
          file_path = '/media/data/folder/tmp/example.jpg',
          filename= 'example.jpg',
          do_not_delete = True,
          extension_isvalid=["png"]
      )

      result = {
          "url": "",
          "local_host":"",
          "filename": ""
      }
    ```
- Version: 0.2.14: Bổ sung thêm cấu hình kafka_bootstrap_servers trong config, cho phép nhập thông tin kafka_brokers. Nếu không nhập option này sẽ tự động lấy từ ENV KAFKA_BROKERS
    - Hướng dẫn sử dụng
    ```python3
      from mobio.sdks.media.mobio_media_sdk import MobioMediaSDK
      MobioMediaSDK().config(
        redis_uri="",
        admin_host="",
        cache_prefix="",
        kafka_bootstrap_servers=os.environ.get("KAFKA_BROKERS")
      )
    ```