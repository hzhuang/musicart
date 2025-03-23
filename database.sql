-- Create 3 tables in music_terms.db
DROP TABLE IF EXISTS composers;
DROP TABLE IF EXISTS terms;
DROP TABLE IF EXISTS review_list;


CREATE TABLE composers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bio TEXT NOT NULL,
    audio_path TEXT  -- for audio files
);

--add terms 
INSERT INTO composers (name, bio, audio_path) VALUES
('Ludwig van Beethoven', 'German composer and pianist. Crucial figure in the transition between classical and romantic eras. Known for symphonies like the 5th and 9th.', 'https://open.spotify.com/embed/track/1BjqQ4UYfV9bOKOvaLxi6n?utm_source=generator'),
('Claude Debussy', 'French composer associated with impressionist music. Famous works include "Clair de Lune" and "La Mer".', 'https://open.spotify.com/embed/track/5qmtIGToI36Z9sNE7bvghH?utm_source=generator');


CREATE TABLE terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT NOT NULL,
    definition TEXT NOT NULL
);

--add terms
INSERT INTO terms (term, definition) VALUES
('Sonata', 'A composition for one or more solo instruments, typically in three or four movements of contrasting forms and keys.'),
('Arpeggio', 'Playing the notes of a chord in succession, either ascending or descending.');

CREATE TABLE review_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_id INTEGER NOT NULL,
    category TEXT NOT NULL, -- term or composer
    term_name TEXT NOT NULL,
    definition_bio NOT NULL,
    your_answer NOT NULL
);

INSERT INTO review_list (reference_id, category, term_name, definition_bio, your_answer) VALUES
(1, 'term', 'Sonata', 'A composition for one or more solo instruments, typically in three or four movements of contrasting forms and keys.', 'test'),  -- User got Beethoven's term "Sonata" wrong
(2, 'composer', 'Claude Debussy', 'French composer associated with impressionist music. Famous works include "Clair de Lune" and "La Mer".', 'wrong'); -- User misidentified Debussy's audio example