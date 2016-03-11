package main

import (
	"fmt"
	"regexp"
)

type VerbalExpression struct {
	RawSource string
}

func newVerbalExpression() *VerbalExpression {
	return &VerbalExpression{""}
}

func (this *VerbalExpression) Compile() *regexp.Regexp {
	return regexp.MustCompile(this.rawSource)
}

func (this *VerbalExpression) StartOfLine() *VerbalExpression {
	this.rawSource += "^"
	return this
}

func (this *VerbalExpression) Maybe(letter string) *VerbalExpression {
	this.rawSource += fmt.Sprintf("(%s)?", regexp.QuoteMeta(letter))
	return this
}

func (this *VerbalExpression) Find(word string) *VerbalExpression {
	this.rawSource += fmt.Sprintf("(%s)", regexp.QuoteMeta(word))
	return this
}

func (this *VerbalExpression) AnythingBut(letter string) *VerbalExpression {
	this.rawSource += fmt.Sprintf("[^%s]*", regexp.QuoteMeta(letter))
	return this
}

func (this *VerbalExpression) EndOfLine() *VerbalExpression {
	this.rawSource += "$"
	return this
}

func (this *VerbalExpression) Match(word string) [][][]byte {
	return this.Compile().FindAllSubmatch([]byte(word), -1)
}

func (this *VerbalExpression) Source() string {
	return this.rawSource
}

func main() {
	v := newVerbalExpression()
	a := v.StartOfLine().Find("http").Maybe("s").Find("://").Maybe("www.").AnythingBut(" ").EndOfLine()
	testUrl := "https://www.google.com"
	if a.Match(testUrl) != nil {
		fmt.Println("Valid URL")
	} else {
		fmt.Println("Invalid URL")
	}

	fmt.Println(a.Source())
}
