from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoModel, AutoTokenizer
import torch

def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=100,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
            "",
        ],
    )
    result = text_splitter.split_text(text)
    for i, part in enumerate(result):
        print(f"Part {i+1}: '{part}' (Length: {len(part)})")
    return result
def embeddings(text):
    model_path = "/Users/trunghuynh/History_chatbot/history_chatbot/models/vietnamese-bi-encoder"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModel.from_pretrained(model_path)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0] #First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    def get_embeddings(text_list):
        encoded_input = tokenizer(
            text_list, padding=True, truncation=True, return_tensors="pt",
        )
        input_ids = encoded_input["input_ids"]
        length = input_ids.shape[1] 
        print(length)

        encoded_input = {k: v.to(device) for k, v in encoded_input.items()}
        model_output = model(**encoded_input)
        return mean_pooling(model_output, encoded_input['attention_mask'])
    
    emb = get_embeddings(text).detach().cpu().numpy()
    return emb

if __name__=="__main__":
    text="""Nhà Trần chuẩn_bị và tiến_hành khang chiến chống quân Mông_Cổ : Cuối năm 1257 , khi được tin quân Mông_Cổ chuẩn_bị xâm_lược , nhà Trần đã ban lệnh cho cả nước sớm sửa vũ_khí , các đội dân binh được thành_lập , ngày_đêm luyện_tập võ_nghệ , sẵn_sàng đánh giặc . Tháng 1 - 1258 , 3 vạn quân Mông_Cổ do Ngô_Thế Lương_Hợp Thái chỉ_huy tiến vào xâm_lược nước ta . Quân giặc theo đường sông Thao tiến xuống Bạch_Hạc ( Việt_Trì , Phú_Thọ ) , rồi tiến đến vùng Bình_Lệ_Nguyên ( Vĩnh_Phúc ) thì bị chặn lại ở phòng tuyển do vua Trần_Thái_Tông trực_tiếp chỉ_huy . Tại đây , một trận đánh quyết_liệt đã diễn ra . Do_thế giặc mạnh , vua Trần cho lui quân để bảo_toàn_lực_lượng . Triều_đình tạm rời kinh_thành Thăng_Long , xuôi về vùng Thiên_Mạc ( Duy_Tiên , Hà_Nam ) . Nhân_dân Thăng_Long , theo lệnh triều_đình , nhanh_chóng thực_hiện chủ_trương ' vườn không nhà trống ' để đánh giặc , tạm rút khỏi kinh_thành . Ngô_Thế Lương_Hợp Thái kéo quân vào Thăng_Long trống_vắng , không một bóng người và lương_thực . Quân Mông_Cổ điên_cuồng tàn_phá kinh_thành , lùng bắt , giết_hại những người còn sót lại . Trước_thế giặc mạnh , tàn_bạo , vua Trần lo_lắng hỏi ý_kiến của Thái_sư Trần Thủ_Độ . Ông trả_lời : ' Đầu thần chưa rơi xuống đất , xin bệ_hạ đừng lo . ' ( Đại_Việt sử_ký toàn thư ) . Đóng giữ kinh_thành Thăng_Long chưa đầy một tháng , quân Mông_Cổ lâm vào tình_thế khó_khăn vì thiếu lượng thực trầm_trọng , phải cho quân_lính đi cướp thóc_gạo , hoa_màu của dân , nhưng nhân_dân các làng , xã đã chống_trả quyết_liệt nên lực_lượng của chúng bị tiêu_hao dần . Nắm được thời_cơ , quân_đội nhà Trần mở cuộc phản_công lớn ở Đông_Bộ Đầu ( bên sông Hồng , ở phố Hàng_Than - Hà_Nội ngày_nay ) . Ngày 29 - 1 - 1258 , quân Mông_Cổ thua trận , phải rút khỏi Thăng_Long . Trên đường rút chạy , chúng bị quân_đội nhà Trần truy_kích . Đến vùng Quy_Hoá ( Yên_Bái , Lào_Cai ) , lại bị quân của Hà_Bổng chặn đánh , quân giặc hoảng tháo_chạy về nước . Cuộc kháng_chiến chỉ diễn ra trong vòng chưa đầy một tháng đã kết_thúc thắng_lợi ."""

    result = split_text(text)
    # emb = embeddings(text)
    # print(emb)
    print(result)
    print(len(result))
