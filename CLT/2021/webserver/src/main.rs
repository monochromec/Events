// Updated example from gist.github.com/mjohnsullivan/e5182707caf0a9dbdf2d
// now invoking external program for content generation

use std::net::{TcpStream, TcpListener};
use std::io::{Read, Write};
use std::thread;
use std::process::Command;

fn main() {
    let listener = TcpListener::bind("0.0.0.0:8080").unwrap();
    println!("Listening for connections on port {}", 8080);

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                thread::spawn(|| {
                    handle_client(stream)
                });
            }
            Err(e) => {
                println!("Unable to connect: {}", e);
            }
        }
    }
}

fn handle_client(stream: TcpStream) {
    handle_read(&stream);
    handle_write(stream);
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

fn handle_write(mut stream: TcpStream) {
    let outp = Command::new("/usr/games/fortune").output().unwrap();
    let out = String::from_utf8_lossy(&outp.stdout);
    let resp = format!("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n<html>\
        <body>{}</body></html>\r\n", out);
    let response = resp.as_bytes();
    match stream.write(response) {
        Ok(_) => println!("Response sent"),
        Err(e) => println!("Failed sending response: {}", e),
    }
}
