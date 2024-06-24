import thumbsUp from "$lib/assets/thumbsUp.png";
import thumbsDown from "$lib/assets/thumbsDown.png";
import thumbNeutral from "$lib/assets/thumbNeutral.png";

export function chooseThumb(sentiment: number){
    if(sentiment > 0){
        return thumbsUp;
    } else if (sentiment < 0){
        return thumbsDown;
    } else {
        return thumbNeutral;
    }
}