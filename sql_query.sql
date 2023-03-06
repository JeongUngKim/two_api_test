use two_db;

select * from contentLike;

truncate contentReview;

-- 검색
select * from content where type = "tv" 
limit 0, 10;


-- 내가 찜한 컨텐츠 삭제하기
delete from contentLike 
where contentId = 1 and contentLikeUserId = 1 ;

-- 내가 찜한 컨텐츠만 보여주기
select * from contentLike;
 
select cl.contentId,cl.contentLikeUserId,c.title,c.genre,c.content,c.imgUrl,c.contentRating,c.createdYear,c.tmdbcontentId 
from contentLike cl join content c 
on cl.contentId = c.Id; 

-- 컨텐츠 리뷰 작성 
select * from contentReview;

insert into contentReview(contentId,contentReviewUserId, title,content,userRating)
values("1","1","행복합니다 나는 ㅠㅠ","행복한거 맞지?","5");

-- 컨텐츠 리뷰 수정 

-- 컨텐츠 리뷰 삭제

-- 컨텐츠 리뷰 좋아요

-- 컨첸츠 리뷰 

-- 컨텐츠 리뷰 댓글 달기

-- 컨텐츠 리뷰 댓글 삭제
 

