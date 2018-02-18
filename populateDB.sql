insert into user (username, email, pw_hash)
values ('son', 'son@gmail.com', 'pbkdf2:sha256:50000$gkk5z9F4$2513d6f712e7a455d040bdbc88eb8528df0dd4c71978d848cdda8546a95accca');
insert into user (username, email, pw_hash)
values ('duy', 'duy@gmail.com', 'pbkdf2:sha256:50000$gkk5z9F4$2513d6f712e7a455d040bdbc88eb8528df0dd4c71978d848cdda8546a95accca');
select * from user;
insert into user (username, email, pw_hash)
values ('mike', 'mike@gmail.com', 'pbkdf2:sha256:50000$gkk5z9F4$2513d6f712e7a455d040bdbc88eb8528df0dd4c71978d848cdda8546a95accca');
insert into user (username, email, pw_hash)
values ('tom', 'tom@gmail.com', 'pbkdf2:sha256:50000$gkk5z9F4$2513d6f712e7a455d040bdbc88eb8528df0dd4c71978d848cdda8546a95accca');
insert into user (username, email, pw_hash)
values ('thomas', 'thomas@gmail.com', 'pbkdf2:sha256:50000$gkk5z9F4$2513d6f712e7a455d040bdbc88eb8528df0dd4c71978d848cdda8546a95accca');

insert into follower (who_id, whom_id)
values (1, 2);
insert into follower (who_id, whom_id)
values (1, 3);
insert into follower (who_id, whom_id)
values (2, 1);
insert into follower (who_id, whom_id)
values (3, 1);
insert into follower (who_id, whom_id)
values (2, 3);
insert into follower (who_id, whom_id)
values (4, 2);
insert into follower (who_id, whom_id)
values (1, 4);

insert into message (message_id, author_id, text)
values (1, 2, 'Hi everyone, my name is Duy');
insert into message (message_id, author_id, text)
values (2, 1, 'Hello, have a nice day');
insert into message (message_id, author_id, text)
values (3, 4, 'Hello, this is Tom, from CSUF');
insert into message (message_id, author_id, text)
values (4, 3, 'Hello, I am also from CSUF');







