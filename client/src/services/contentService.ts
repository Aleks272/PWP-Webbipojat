import axios from "axios";

import { API_URL } from "../constants";
import { Content } from "../types/Content";

const getContent = async (contenId: number): Promise<Content> =>
    (await axios.get(`${API_URL}/content/${contenId}/`)).data

export default {
    getContent
}