// Small bookshop simulation
// Inspired by gist.github.com/mjohnsullivan/e5182707caf0a9dbdf2d


//
// (c) 2021 by Chris Zimmermann
//

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
use std::net::{TcpStream, TcpListener};
use std::io::{Read, Write};
// use std::thread;
use serde::{Serialize};
use serde_json;
use rand::Rng;
use crossbeam;

#[derive(Serialize, Debug)]
struct Book {
    author: String,
    title: String,
    year: u32,
    price: f32,
}

fn fill_shelve() -> Vec<Book> {
    let book1 = Book {
        author: "Herman Melville".to_string(),
        title: "Moby-Dick".to_string(),
        year: 1851,
        price: 15.29,
    };
    let book2 = Book {
        author: "Mark Twain".to_string(),
        title: "The Adventures of Tom Sawyer".to_string(),
        year: 1876,
        price: 12.19,
    };
    let book3 = Book {
        author: "Edgar Allen Poe".to_string(),
        title: "The Lighthouse".to_string(),
        year:  1849,
        price: 9.52,
    };
    let book4 = Book {
        author: "Ernest Hemingway".to_string(),
        title: "The Old Man and the Sea".to_string(),
        year:  1958,
        price: 11.48,
    };

    vec![book1, book2, book3, book4]
}

fn main() {
    let books = fill_shelve();
    // Prepare shelf to pick books from
    let mut shelf = Vec::new();
    for i in books {
        shelf.push(serde_json::to_string(&i).unwrap().clone());
    }
    let listener = TcpListener::bind("0.0.0.0:8080").unwrap();
        println!("Listening for connections on port {}", 8080);

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                crossbeam::scope(|scope| {
                    scope.spawn(|_| {
                        handle_client(stream, &shelf);
                    });
                }).unwrap();
            }
            Err(e) => {
                println!("Unable to connect: {}", e);
            }
        }
    }
}

fn handle_client(stream: TcpStream, shelf: &[String]) {
    handle_read(&stream);
    handle_write(stream, shelf);
}

fn handle_read(mut stream: &TcpStream) {
    let mut buf = [0u8; 4096];
    match stream.read(&mut buf) {
        Ok(_) => {
            let req_str = String::from_utf8_lossy(&buf);
            println!("{}", req_str);
            },
        Err(e) => println!("Unable to read stream: {}", e),
    }
}

fn handle_write(mut stream: TcpStream, shelf: &[String]) {
    let len = shelf.len();
    // Pick random book
    let mut rng = rand::thread_rng();
    let n0 = rng.gen_range(0..len);
    let n1 = rng.gen_range(0..len);
    let ndx = (n0 * n1) % len;  
    let book = shelf[ndx].clone();
    let resp = format!("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<html>\
        <body>{}</body></html>\r\n", book);
    let response = resp.as_bytes();
    match stream.write(response) {
        Ok(_) => println!("Response sent"),
        Err(e) => println!("Failed sending response: {}", e),
    }
}
