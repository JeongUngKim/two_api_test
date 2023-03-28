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

select * from actor;
insert into actor(contentId,name,year)
values(1,"범죄입니다","2020-01-02");

-- 컨텐츠 찜하기
select * from contentLike;

insert into contentLike(contentId,contentLikeUserId)
values(553,1);

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
where contentReviewId = 1 ;

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
delete from contentReviewLike 
where contentReviewId = 1 and contentReviewLikeUserId = 1 ;

-- 컨텐츠 리뷰 댓글 달기
select * from contentReviewComment;

insert into contentReviewComment(contentReviewId , commentUserId , comment )
values ("1","1","완전대박!!!");

-- 컨텐츠 리뷰 댓글 삭제
delete from contentReviewComment
where commentId = 2 and contentReviewId = 1 and commentUserId = 1;

select * from contentReviewComment;
-- 컨텐츠 리뷰 댓글 수정

update contentReviewComment
set comment = ""
where commentId = 1 and contentReviewId = 1 and commentUserId = 1;

-- 회원가입시 유저 장르 설정

insert into userGenre(userId,tagId)
values("1","1");

-- 유저 정보 수정
select * from user;
update user
set nickname="",password = "",profileimgUrl=""
where id = 1;

-- 유저 회원 탈퇴
select * from user;

delete from user
where id = 2;


-- 내가 본 컨텐츠 insert
select * from contentWatchme;
insert into contentWatchme(userId,contentId)
values("1","1");

-- 내가 본 컨텐츠 목록 가져오기

select cw.userId,cw.contentId,c.title,c.imgUrl,c.contentRating,c.tmdbcontentId,c.type
from contentWatchme cw 
join content c 
on cw.contentId = c.Id
where cw.userId = 1;

-- 컨텐츠 가져오기
select * from content;
select * from contentLike;
select * from user;

select c.*, if(cl.contentLikeUserId = null  , 0 , 1 ) as 'like'
from content c left join contentLike cl
on  c.id = cl.contentId
where c.id = 553;

-- 컨텐츠 리뷰 가져오기
select * from contentReview;
select * from contentReviewLike;

select cr.*, count(crl.contentReviewLikeUserId) as likeCnt
from contentReview cr left join contentReviewLike crl
on cr.contentReviewId = crl.contentReviewId 
where cr.contentId = 553
group by contentReviewId;


insert into contentReviewLike(contentReviewId,contentReviewLikeUserId)
values(2,3);

select *
from contentReview
where contentId = 553;
-- 내가 작성한 컨텐츠 리뷰 가져오기

select contentReviewId,contentId,title,content,userRating,createdAt,updatedAt
from contentReview
where contentReviewUserId = 3;
select * from user;
-- 컨텐츠 리뷰 댓글 가져오기
select *
from contentReviewComment
where contentReviewId = 1;

-- 파티 글 작성
select * from partyBoard;

insert into partyBoard(service,title,userId,serviceId,servicePassword)
values("Netflix","넷플구독자구함",1,"abc@naver.com","1234");

-- 파티 글 전체 가져오기

select partyBoardId,service,title,content,createdAt,userId from partyBoard; 

-- 내 파티 글 수정
select * from partyBoard where partyBoardId = 1 and userId = 1;

update partyBoard
set service = "",title = "" , content = "" , serviceId = "", servicePassword = ""
where partyBoardId = 1 and userId = 1;

-- 내 파티 글 삭제

select * from partyBoard;

delete from partyBoard
where partyBoardId = 2 and userId = 1;

-- 파티 글 검색
select pb.*,count(member) as memberCnt 
from partyBoard pb left join party p 
on pb.partyBoardId = p.partyBoardId 
where pb.title like "%아마존%" or pb.service like "%Netflix%"
group by partyBoardId;

select * from partyBoard;
delete from partyBoard where partyBoardId = 4;
-- 파티 맺기 ( 결제 완료 )
select * from party;

select userId ,service , finishedAt from partyBoard where partyBoardId = 5;

insert into party(captain , member , partyBoardId )
values(1,5,5);
select * from paymentDetails;

insert into paymentDetails(partyBoardId,userId,amount,date)
values(3,2,4250,'2023-03-04');

select * from paymentDetails;

-- 내가 맺은 파티 항목 전체 가져오기
select p.captain,p.partyBoardId,p.createdAt,pb.service,pb.title,pb.content,pb.serviceId,pb.servicePassword,pb.finishedAt
from party p 
left join partyBoard pb 
on p.partyBoardId = pb.partyBoardId
where member = 3;
-- 내가 맺은 파티 일부 항목 가져오기

-- 파티 맺기 취소 ( 결제 취소 )
delete from party
where member = 2 and partyBoardId = 5;

-- 파티 완료 여부 확인

select count(member) as memberCnt from party
where partyBoardId = 5 
group by partyBoardId;

-- 
select * from actor;

--
select * from content
limit 10 , 10 ;


select * from user;

-- 조회수 톱 20 
select c.*,count(cm.contentId) as cnt
from contentWatchme cm right join content c
on cm.contentId = c.id 
group by c.id
order by cnt desc
limit 0, 20;

select * from content where title like '%원피스%';

select * from actor;
        
insert into contentWatchme(userId,contentId)
values(5,424);

--
select * from partyBoard;
-- 48 , 1
select * from party;

delete from party
where captain = 1 and member = 4content_test;

-- 커뮤니티 테이블 글 작성
select * from community;

insert into community(userId,title,content,imgUrl)
values(3,"알랑캉","반갑습니다.","https:");

-- 커뮤니티 테이블 글 수정
update community
set title = "안녕못해!" , content = "반갑지않거덩?", imgUrl = "123"
where userId = "1" and communityId = "1";

-- 커뮤니티 테이블 글 삭제
delete from community
where communityId = "1" and userId = "1";

select * from community;

-- 커뮤니티 전체 글 가져오기
select cm.*,u.nickname,u.userEmail,u.profileImgUrl
from community cm join user u
on cm.userId = u.id 
limit 0 , 100;

select * from communityLike;

-- 커뮤니티 내가 쓴 글 가져오기
select cm.*,u.nickname,u.userEmail,u.profileImgUrl
from community cm join user u
on cm.userId = u.id
where cm.userId = 3
limit 0 , 100;

-- 커뮤니티 검색(title or content)
select cm.*,u.nickname,u.userEmail,u.profileImgUrl 
from community cm join user u
on cm.userId = u.id
where title like "%반갑%" or content like "%반갑%"
limit 0 , 10;

-- 좋아요 추가
select * from community;

select * from communityLike;

insert into communityLike(communityId,userId)
values(5,4);

-- 좋아요 취소
delete from communityLike
where communityId= 3 and userId = 5; 

-- 
select * from partyBoard;

select * from user;

select * from party;

select * from actor;

select * from content
where title like "%아바타%" ;

select * from actor where name = '마동석';


select * from actor
where tmdbcontentIdList like "%19995%";

select * from community;

select * from partyBoard;

select * from party;

truncate paymentDetails;

delete from partyBoard
where partyBoardId = 16;

delete from community
where communityId not in (23,24,25);

select pb.userId,pb.service,pb.serviceId,pb.servicePassword,pb.finishedAt,u.userEmail
                        from party p join partyBoard pb
                        on p.partyBoardId = pb.partyBoardId join user u
                        on p.member = u.id
                        where p.partyBoardId =
                    ;    
select * from party;

select * from partyBoard;
insert into party(captain,member,partyBoardId)
values(45,1,2);
-- party 1 user 21 ad 2 , 45

select * from partyBoard;

select * from party;

select * from contentWatchme;