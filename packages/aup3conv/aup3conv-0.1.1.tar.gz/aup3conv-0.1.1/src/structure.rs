use std::io;
use pyo3::prelude::*;
use crate::tagstack::Tag;
// pub struct Project {
//     xmlns: String,
//     version: String,
//     audacityversion: String,
//     sel0: f64,
//     sel1: f64,
//     vpos: u8,
//     h: f64,
//     zoom: f64,
//     rate: i32,
//     snapto: String,
//     selectionformat: String,
//     frequencyformat: String,
//     bandwidthformat: String,
//     tracks: Vec<Tracks>,
// }


// pub struct Effects {
//     active: bool,
// }
//
// enum Tracks {
//     WaveTrack(WaveTrack),
//     LabelTrack(LabelTrack),
// }
//
// pub struct WaveTrack {
//     name: String,
//     isSelected: bool,
//     height: i16,
//     minimized: bool,
//     channel: u8,
//     linked: u8,
//     mute: bool,
//     solo: bool,
//     rate: i32,
//     gain: f64,
//     pan: f64,
//     colorindex: i32,
//     sampleformat: i64,
//     clips: Vec<WaveClip>,
// }
//
#[derive(Debug, Clone)]
#[pyclass]
pub struct WaveClip {
    #[pyo3(get)]
    pub offset: f64,
    trim_left: Option<f64>,
    trim_right: Option<f64>,
    name: Option<String>,
    colorindex: Option<i32>,
    #[pyo3(get)]
    pub sequences: Option<Sequence>
    //envelope: Option<Envelope>,
}

impl WaveClip {
    pub fn from_tag(tag: &Tag) -> io::Result<Self> {
        let offset = tag.attributes.get("offset")
            .expect("Key 'offset' not in tag attributes")
            .parse::<f64>().unwrap();

        Ok(Self { offset: offset, trim_left: None, trim_right: None,
            name: None, colorindex: None, sequences: None })
    }

    pub fn is_empty(&self) -> bool {
        if let Some(seq) = &self.sequences {
            if seq.numsamples > 0 { false } else { true }
        } else {
            false
        }
    }
}

#[pymethods]
impl WaveClip {
    fn __str__(&self) -> String {
        format!("WaveClip(offset={}, trim_left={:?}, trim_right={:?},
            name={:?}, colorindex={:?}, sequences={:?})",
        self.offset, self.trim_left, self.trim_right, self.name, self.colorindex,
        self.sequences)
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }
}

#[derive(Debug, Clone)]
#[pyclass]
pub struct Sequence {
    pub maxsamples: u64,
    pub sampleformat: u64,
    pub numsamples: u64,

    #[pyo3(get)]
    pub blocks: Vec<WaveBlock>
}

impl Sequence {
    pub fn from_tag(tag: &Tag) -> io::Result<Self> {
        let maxsamples = tag.attributes.get("maxsamples")
            .expect("Key 'start' not in tag attributes")
            .parse::<u64>().unwrap();

        let sampleformat = tag.attributes.get("sampleformat")
            .expect("Key 'start' not in tag attributes")
            .parse::<u64>().unwrap();

        let numsamples = tag.attributes.get("numsamples")
            .expect("Key 'start' not in tag attributes")
            .parse::<u64>().unwrap();

        Ok(Self { maxsamples: maxsamples, sampleformat: sampleformat,
            numsamples: numsamples, blocks: Vec::<WaveBlock>::new() })
    }

    //pub fn new() -> Self {
    //    Self { maxsamples: 0, sampleformat: 0, numsamples: 0, blocks: Vec::<WaveBlock>::new() }
    //}
}

#[pymethods]
impl Sequence {
    fn __str__(&self) -> String {
        format!("Sequence(maxsamples={}, sampleformat={}, numsamples={})",
        self.maxsamples, self.sampleformat, self.numsamples)
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }
}

#[derive(Debug,Clone)]
#[pyclass]
pub struct WaveBlock {
    #[pyo3(get)]
    pub start: usize,

    #[pyo3(get, name="block_id")]
    pub blockid: u16,
}

impl WaveBlock {
    pub fn from_tag(tag: &Tag) -> io::Result<Self> {
        let start = tag.attributes.get("start")
            .expect("Key 'start' not in tag attributes")
            .parse::<usize>().unwrap();
        let bid = tag.attributes.get("blockid")
            .expect("Key 'blockid' not in tag attributes")
            .parse::<u16>().unwrap();
        Ok(Self { start: start, blockid: bid })

    }
}

#[pymethods]
impl WaveBlock{
    fn __str__(&self) -> String {
        format!("WaveBlock(block_id={}, start={})", self.blockid, self.start)
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }
}
//
// pub struct Envelope {
//     numpoints: u64,
// }
//
// pub struct LabelTrack {
//     name: String,
//     isSelected: bool,
//     height: i16,
//     minimized: bool,
//     numlabels: i32,
//     labels: Vec<Label>,
// }

#[derive(Debug)]
#[derive(Clone)]
#[pyclass]
pub struct Label {
    #[pyo3(get, name="start")]
    pub t: f64,

    #[pyo3(get, name="stop")]
    pub t1: f64,

    #[pyo3(get)]
    pub title: String,
}

impl Label {
    pub fn from_tag(tag: &Tag) -> io::Result<Self> {
        let title = tag.attributes.get("title")
            .expect("Key 'title' not in tag attributes");
        let t = tag.attributes.get("t")
            .expect("Key 't' not in tag attributes")
            .parse::<f64>().unwrap();
        let t1 = tag.attributes.get("t1")
            .expect("Key 't1' not in tag attributes")
            .parse::<f64>().unwrap();
        Ok(Self { title: title.clone(), t: t, t1: t1 })
    }
}

#[pymethods]
impl Label {
    fn __str__(&self) -> String {
        format!("Label(title='{}', start={}, stop={})", self.title, self.t, self.t1)
    }

    fn __repr__(&self) -> String {
        self.__str__()
    }
}
