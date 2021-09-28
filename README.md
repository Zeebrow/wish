# wish

Use a markdown file to keep a list of projects you want to do.

plan is to take out a slight chunk of `src/wishlist` and make a markdown db.
so, tests are not going to be written against anything click-related.

## Usage

```
Usage: wish [OPTIONS] COMMAND [ARGS]...

  Keep track of your list of projects you want to do.

  Wishes are managed by reading to and writing from wishlist.md. When you
  make a wish, you provide the name for the command you want to make. You
  can optionally edit a block of markdown to provide more details on your
  idea.

  When the markdown file is saved, wishlist.md and the project skeleton
  directory are committed to git.

Options:
  --help  Show this message and exit.

Commands:
  del
  edit
  get
  ls    list all current wishes
  make
```

## Install 

```bash
pip install -e
```

# algorithm concept

This is the plan for the refactor.

## the lastmiles approach

Inspired by friendly C programmer and greybeard [lastmiles](https://www.youtube.com/user/lastmiles).

Linux philosophers, avert your eyes - for the time being, this program is
going to say a LOT more than what's necessary. Hopefully it fails just as noisily.

The approach I want to take making this program consists of three parts:

1. Tell me what you (the program) are about to do
2. Do the thing
3. Tell me what you (the program) just did.

Very clear, indeed! Tuning the log levels can come later; for now, 
logger actions are level `INFO`. For now, both info and warning+ logging levels
will be printed to `stdout`. 

## raw data is easily readable and shareable

A `wish` is just a block of markdown text that begins with an `h2` block.

## ... at the expense of speedy operations (and possibly memory) 

When a new `wish` object is made, it ingests the entire wishlist,
`constants.wishlist`, into memory: every wish has a `wish.block`, 
`wish.before`, and `wish.after`, corresponding to the text in the
file

Every wish is represented by such a `wish.block`. 
The `h2` heading of the markdown determines the name of the wish,
`wish.name`. This is displayed when running `wish ls`, and what
is used to print a `wish.block` wish `wish get WISHNAME`

## CRUD

CRUD operations are 'atomic' in the sense that these operations
only ever act on a single wish at time. Write operations end with
a `git commit`. 

### Create 

`wish make WISHNAME`

Appends to the end of the wishlist, a default 'skeleton' wish.

The wishlist is re-written and committed as 

```bash
wishlist.make(WISHNAME) := wish.before + wish.block + wish.after
```

where `wish.after` is an empty string.

### Read

returns `wish.block`, which is found by searching the file
for the regex `^##\s+(.*)$`


### Update

returns `wish.block` to the user using the terminal's default
editor, using `click.edit`.

Changes to `wish.block` are saved in memory, and persisted with

```bash
wishlist.edit(WISHNAME) = wish.before + wish.block + wish.after
```

### Delete

Removes `wish.block` from `wishlist.md` by setting `wish.block` to
an empty string

```bash
wishlist.del(WISHNAME) := wish.before + wish.block + wish.after 
```
