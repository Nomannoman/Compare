import { apicaller } from "./axios";

export const getAmazonHTML = async(
    plusURL,
)=>{
    const res = await apicaller.get(`/amazon/${plusURL}`,
    );
    return res;
}