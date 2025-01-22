# `txttree`
`txttree` is a tool for organizing and displaying hierarchical relationships using a file-based structure and text files.
Basically, `txttree` is like `tree` for text files with some added features for interpreting file contents like properties and values.

## Example
`txttree` can be used to maintain information or organizational structure in a text based format.
For example, we could display the structure of Easy Company, a U.S. Army unit which was described in the series Band of Brothers.

```
$ python -m txttree "test/Easy Company"
Easy Company
│ CO: Capt. Richard Winters   (1944-06-07)
│ XO: 1st Lt. Harry Welsh   (1944-06-08)
│ First Sergeant: SFC Carwood Lipton   (1944-06-08)
├─ 1st Platoon
│  │ Platoon Leader: 1st Lt. Thomas Peacock
│  │ Assistant Leader: 2nd Lt. Charles Hudson
│  │ Platoon Sergeant: SFC Floyd Talbert
│  ├─ 1st Squad
│  ├─ 2nd Squad
│  ├─ 3rd Squad
│  └─ Mortar Squad
├─ 2nd Platoon
│  │ Platoon Leader: 1st Lt. Lynn Compton
│  │ Assistant Leader: 2nd Lt. John Pisanchin
│  │ Platoon Sergeant: SFC William Guarnere
│  ├─ 1st Squad
│  ├─ 2nd Squad
│  ├─ 3rd Squad
│  └─ Mortar Squad
└─ 3rd Platoon
   │ Platoon Leader: 1st Lt. Robert Brewer
   │ Assistant Leader: 2nd Lt. Ben Perkins
   │ Platoon Sergeant: SFC Amos Taylor
   ├─ 1st Squad
   ├─ 2nd Squad
   ├─ 3rd Squad
   └─ Mortar Squad
```

The `txttree` command takes a root folder: in this case `test/Easy Company`.
`txttree` then recurses through the directory structure and prints the contents of folders and properties in text files, like the `tree` command in linux.
See below how `txttree` interprets text files.
The example data is in the `test/` folder in this repository.

## Usage
```
 Usage: python -m txttree [OPTIONS] ROOT_DIRECTORY_PATH                         

╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    root_directory_path      PATH  Root directory for the hierarchy.        │
│                                     [default: None]                          │
│                                     [required]                               │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## File and folder structure
`txttree` uses folder structure for the hierarchy and the information in text files for the properties.
All text files (with extension `.txt`) in subfolders will be searched for properties and displayed as a node.
The text files describe data in a log-style format.

This is an example of a text file with parameters that can be interpreted by `txttree`.
This fictional example file describes the structure of Easy Company in a log.
```
The command structure of Easy Company is as follows:
CO: 1st Lt. Thomas Meehan
XO: 1st Lt. Richard Winters
First Sergeant: William Evans

1944-06-06
It is D-Day.
The landings have begun.

1944-06-07
No sign of 1st Lt. Thomas Meehan.
Capt. Richard Winters assumes the role of commanding officer.
CO: Capt. Richard Winters
```
This file demonstrates three possible line types in a text file:
* A **property** is a line in a text file that starts with a property key like "_CO_", a colon "_:_" and a property value like "_1st Lt. Thomas Meehan_".
  For example: `CO: 1st Lt. Thomas Meehan`.
  You are free to chose which property keys make sense for your use case.
  * If the same property is defined multiple times in the file, the last value of the property is taken.
    This makes it easy to update data in the future.
  * A property key can be one to three words long.
* An optional **date line** indicates the date of the text or properties.
  The date will be shown in `txttree` output in parentheses after the property, for example: `CO: Capt. Richard Winters   (1944-06-07)`.
  A date line can be in three formats:
  * ISO format: for example "1944-06-06",
  * Short format: for example "440606",
  * Long format: for example "19440606".
* A normal text line, which is neither a property nor a date line.
  Normal text lines are ignored by `txttree`. 

Text files in a folder will be displayed as separate nodes.
The only exception is a text file with the same name as the parent folder: these properties are displayed under the parent folder.