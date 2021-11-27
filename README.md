# Brutal Searcher

Brutal Searcher is a string search tool. It can search for files of the specified type containing the specified string in the specified directory. For example, in a Unity project, you can use this tool to find the GUID of an asset in the project directory to see which assets reference this asset. The tool will automatically use the appropriate number of threads for multi-threaded search, so the search speed is fast.

## Usage

Before everything starts, you need to install python3 and clone this repository.

Then use the following command to start the search.

```
python bs.py <directory> <target> <suffix>.
```

Replace `<directory>` with the path you want to search, replace `<target>` with the string you want to search, and replace `<suffix>` with the suffix of the file type you want to specify.

After waiting for a period of time, you can see the search results in the console.

## License

MIT
