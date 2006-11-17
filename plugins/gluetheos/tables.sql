create table sourcefiles (
	filename		varchar(255) not null,
	revision		varchar(16) not null,
	rev_date		date not null,
	rev_time 		time not null,
	content			BLOB,
	clean_content		BLOB,
	sha1			char(40) not null,
	nilsimsa		char(64) not null,
	sha1_clean		char(40) not null,
	nilsima_clean		char(40) not null,
	sloc			int,
	lang			varchar(8),
	output_sloccount	BLOB,
	loc			int,
	output_wc		BLOB,
	functions		int,
	output_ctags		BLOB,
	mccabe			int,
	returns			int,
	length			int,
	volume			int,
	level			float,
	output_halstead		BLOB,
	primary key (filename, revision)
);