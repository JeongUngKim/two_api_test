use two_db;

truncate user;

select * from user;
-- 유저 회원 가입
insert into user(nickname,userEmail,password,gender,age)
values("","","","","");

-- 유저 로그인
select* 
from user
where userEmail="";

-- 유저 아이디 찾기
select * 
from user
where name = "정웅" and questionNum="1" and questionAnswer = "인천";

-- 검색
select * 
from content 
where title like "%%" and type = "movie" and
genre like "%Fantasy%" and genre like "%Ad%" and contentRating >= 0.0 and createdyear >= '2020-05-06'
limit 0, 10
;

-- 컨텐츠 찜하기
select * from contentLike;

insert into contentLike(contentId,contentLikeUserId)
values(1,1);

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

update contentReview 
set title = "수정이지롱" ,content = "수정이지!"
where contentreviewId = 1 ;

select * from contentReview ;
 
-- 컨텐츠 리뷰 삭제
delete from contentReview
where contentReviewId = 2 and contentReviewUserId = 1;

select * from contentReview;
-- 컨텐츠 리뷰 좋아요
select * from contentReviewLike;
insert into contentReviewLike(contentReviewId,contentReviewLikeUserId)
values(1,1);
-- 컨텐츠 리뷰 좋아요 취소

-- 컨텐츠 리뷰 댓글 달기

-- 컨텐츠 리뷰 댓글 삭제

-- 컨텐츠 리뷰 댓글 수정