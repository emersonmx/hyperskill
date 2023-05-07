package main

import (
	"bufio"
	"crypto/md5"
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

type Path struct {
	filesize int64
	filepath string
	hash     string
}

func getFileFormat() string {
	var fileFormat string
	fmt.Println("Enter file format:")
	fmt.Scanln(&fileFormat)
	return strings.TrimSpace(fileFormat)
}

func getSortOption() int {
	fmt.Println()
	fmt.Println(`Size sorting options:
1. Descending
2. Ascending`)

	for {
		fmt.Println()
		fmt.Println("Enter a sorting option:")
		var option int
		_, err := fmt.Scanln(&option)
		validInput := err == nil && (option == 1 || option == 2)
		if validInput {
			return option
		}
		fmt.Println()
		fmt.Println("Wrong option")
	}
}

func getCheckForDuplicates() bool {
	var check string
	for {
		fmt.Println()
		fmt.Println("Check for duplicates?")
		_, err := fmt.Scan(&check)
		check = strings.ToLower(strings.TrimSpace(check))
		validInput := err == nil && (check == "yes" || check == "no")
		if validInput {
			return check == "yes"
		}
		fmt.Println()
		fmt.Println("Wrong option")
	}
}

func getDeleteDuplicates() bool {
	var check string
	for {
		fmt.Println()
		fmt.Println("Delete files?")
		_, err := fmt.Scan(&check)
		check = strings.ToLower(strings.TrimSpace(check))
		validInput := err == nil && (check == "yes" || check == "no")
		if validInput {
			return check == "yes"
		}
		fmt.Println()
		fmt.Println("Wrong option")
	}
}

func getFilesToDelete(paths []Path) []int64 {
	var files []int64
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Println()
		fmt.Println("Enter file numbers to delete:")
		if !scanner.Scan() {
			break
		}

		pathsLength := int64(len(paths))
		rawNumbers := strings.Split(strings.TrimSpace(scanner.Text()), " ")
		for _, s := range rawNumbers {
			number, err := strconv.ParseInt(s, 10, 64)
			validInput := err == nil && 1 <= number && number <= pathsLength
			if validInput {
				files = append(files, number)
			} else {
				fmt.Println()
				fmt.Println("Wrong format")
			}
		}
		break
	}

	err := scanner.Err()
	if err != nil {
		return nil
	}
	return files
}

func displayPathOrderedBySize(paths []Path) {
	var currentSize int64
	currentSize = -1
	for _, path := range paths {
		if currentSize != path.filesize {
			currentSize = path.filesize
			fmt.Printf("\n%d bytes\n", currentSize)
		}
		fmt.Println(path.filepath)
	}
}

func displayDuplicatedPaths(paths []Path) {
	currentSize := int64(-1)
	currentHash := ""
	count := 1
	for _, path := range paths {
		if currentSize != path.filesize {
			currentSize = path.filesize
			fmt.Println()
			fmt.Printf("%d bytes\n", path.filesize)
		}
		if currentHash != path.hash {
			currentHash = path.hash
			fmt.Printf("Hash: %x\n", path.hash)
		}
		fmt.Printf("%d. %s\n", count, path.filepath)
		count++
	}
}

func getDuplicatedPaths(paths []Path) []Path {
	hashCount := make(map[string][]Path)
	for _, path := range paths {
		key := path.hash
		hashCount[key] = append(hashCount[key], path)
	}

	var duplicatedPaths []Path
	for _, paths := range hashCount {
		if len(paths) <= 1 {
			continue
		}
		for _, path := range paths {
			duplicatedPaths = append(duplicatedPaths, path)
		}
	}
	return duplicatedPaths
}

func deleteFiles(files []int64, paths []Path) {
	spaceFreed := int64(0)
	for _, file := range files {
		path := paths[file-1]
		os.Remove(path.filepath)
		spaceFreed += path.filesize
	}

	fmt.Println()
	fmt.Printf("Total freed up space: %d bytes\n", spaceFreed)
}

func sortByFilesize(paths []Path, order int) func(i, j int) bool {
	return func(i, j int) bool {
		switch order {
		case 1:
			return paths[i].filesize > paths[j].filesize
		case 2:
			return paths[i].filesize < paths[j].filesize
		default:
			return paths[i].filesize > paths[j].filesize
		}
	}
}

func main() {
	if len(os.Args) != 2 {
		fmt.Print("Directory is not specified")
		return
	}

	searchPath := os.Args[1]
	fileFormat := getFileFormat()
	sortOption := getSortOption()

	var paths []Path
	filepath.Walk(searchPath, func(path string, info fs.FileInfo, err error) error {
		if info.IsDir() {
			return nil
		}
		if len(fileFormat) > 0 && !strings.HasSuffix(path, fileFormat) {
			return nil
		}

		f, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer f.Close()

		hash := md5.New()
		if _, err := io.Copy(hash, f); err != nil {
			return nil
		}

		paths = append(paths, Path{
			filesize: info.Size(),
			filepath: path,
			hash:     string(hash.Sum(nil)),
		})
		return nil
	})

	sort.Slice(paths, sortByFilesize(paths, sortOption))
	duplicatedPaths := getDuplicatedPaths(paths)
	sort.Slice(duplicatedPaths, sortByFilesize(duplicatedPaths, sortOption))

	displayPathOrderedBySize(paths)

	if getCheckForDuplicates() {
		displayDuplicatedPaths(duplicatedPaths)
	}

	if getDeleteDuplicates() {
		filesToDelete := getFilesToDelete(duplicatedPaths)
		deleteFiles(filesToDelete, duplicatedPaths)
	}
}
