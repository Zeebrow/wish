package main

import (
  "os"
  "strings"
  "fmt"
  "log"
  "bufio"
  "github.com/charmbracelet/glamour"
)

var mdtext []string

func pprint(md string) {
  out, err := glamour.Render(md, "dark")
  if err != nil {
    log.Fatal(err.Error())
  }
  fmt.Print(out)
}

func main() {
  scanner := bufio.NewScanner(os.Stdin)
  for scanner.Scan() {
    mdtext = append(mdtext, scanner.Text() + "\n")
  }

  if scanner.Err() != nil {
    log.Fatal("Something went wrong!\n%s\n", scanner.Err())
  }

  pprint(strings.Join(mdtext, " "))

}
