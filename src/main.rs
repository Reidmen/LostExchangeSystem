#![allow(unused_variables)]

#[derive(Debug)]
struct File {
    name: String,
    data: Vec<u8>,
}
impl File {
    fn new(name: &str) -> File {
        File {
            name: String::from(name),
            data: Vec::new(),
        }
    }
    fn new_with_data(name: &str, data: &Vec<u8>) -> File {
        let mut f = File::new(name);
        f.data = data.clone();
        f
    }
    fn read(self: &File, save_to: &mut Vec<u8>) -> usize {
        let mut tmp = self.data.clone();
        let read_length = tmp.len();
        save_to.reserve(read_length);
        save_to.append(&mut tmp);
        read_length
    }
}

fn open(f: &mut File) -> bool {
    true
}

fn close(f: &mut File) -> bool {
    true
}

fn main() {
    let new_data: Vec<u8> = vec![114, 117, 115, 116, 33, 54];
    let mut new_file = File::new_with_data("logfile.log", &new_data);
    let mut buffer: Vec<u8> = vec![];

    open(&mut new_file);
    let new_file_length = new_file.read(&mut buffer);
    close(&mut new_file);

    let text = String::from_utf8_lossy(&buffer);

    println!("{:?}", new_file);
    println!("{} is {} bytes long", &new_file.name, &new_file_length);
    println!("{}", text)
}
