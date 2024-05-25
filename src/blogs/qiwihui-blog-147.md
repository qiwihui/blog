# CSS 基础──样式篇

《[前端小课──用好HTML](https://lefex.github.io/books/html-book/introduction.html)》的读书笔记。

### 使用css三种方式

1. 外部引入：通过 link 的方式引用 CSS 样式

    ```html
    <head>
    	<link rel="stylesheet" href="style.css">
    </head>
    ```

2. 内部引入，在 HTML 中的 head 位置添加 style 标签

    ```html
    <head>
      <style>
        .title {
          color: red;
          font-size: 18px;
        }
      </style>
    </head>
    ```

3. 内联样式

    ```html
    <p style="color: red; font-size: 18px;">内容</p>
    ```

### 块级标签和 inline 标签

- 块级标签独占一行；
- inline 标签会「累加」，如同打字一样，一个字一个字往后拼接，单行显示不全会折行显示；
    - `white-space` 属性作用就是告诉浏览器遇到「空格」该如何处理，这里的空格不是单纯意义上的空格。
        - `normal`
        - `nowrap`

### `overflow` 属性

- 控制对于超出可视区域的内容如何处理
- `overflow-x` ， `overflow-y`

```css
/* 默认值。内容不会被修剪，会呈现在元素框之外 */
overflow: visible;

/* 内容会被修剪，并且其余内容不可见 */
overflow: hidden;

/* 内容会被修剪，浏览器会显示滚动条以便查看其余内容 */
overflow: scroll;

/* 由浏览器定夺，如果内容被修剪，就会显示滚动条（默认值） */
overflow: auto;

/* 规定从父元素继承overflow属性的值 */
overflow: inherit;
```

### 清除标签默认边距

```css
/*清除标签默认边距*/
* {
    margin: 0;
    padding: 0;
}
```

### CSS中的选择器

![Untitled](https://user-images.githubusercontent.com/3297411/129540047-12aa2048-3121-4d5d-a40d-c4d052a52bbc.png)

注意：写 CSS 代码的时候，即使某个属性写错，浏览器也不会报错，只会忽略无法识别的 CSS 样式。

- 标签选择器： 如 `p` ， `li` 等
- class 选择器：如 `.first`
- ID 选择器： `#firstid`
- 通用选择器： `*` ，作用于所有的标签
- 属性选择器：根据属性来匹配HTML元素

    ```css
    /* 匹配所有使用属性 "lefe" 的元素 */
    [lefe] {
        color: green;
    }

    /*匹配所有使用属性为 "lefe"，且值为 liquid 的元素*/
    [lefe="liquid"] {
        background-color: goldenrod;
    }

    /*匹配所有使用属性为 "lefe"，且值包含 spicy 的元素*/
    [lefe~="spicy"] {
        color: red;
    }
    ```

- 类似于“正则表达式”的属性选择器，比如： `[attr^=val]` 匹配以 val 开头的元素， `[attr$=val]` ,匹配以 val 结尾的元素， `[attr*=val]` 匹配包含 val 的字符串的元素
- 伪选择器（pseudo-selectors）：它包含伪类（pseudo-classes）和伪元素（pseudo-elements）。这类选择器不是真正意义上的选择器，它作为选择器的一部分，起到选择器匹配元素的限定条件。

    ```css
    /* 匹配超链接样式 */
    a {
        color: blue;
        font-weight: bold;
    }

    /* 访问后的状态 */
    a:visited {
        color: yellow;
    }

    /* 鼠标悬停、点击、聚焦时的样式 */
    a:hover,
    a:active,
    a:focus {
        color: darkred;
        text-decoration: none;
    }
    ```

    - 伪元素（pseudo-elements）选择器，它以“ :: ” 为标识符

        ```css
        p::first-letter{
          font-weight: bold;
        }
        p::first-line{
          font-size: 3em;
        }
        ```

        ```css
        /* Selects any <p> that is the first element
           among its siblings 
        	 p:first-child 选择的是孩子节点中第一个元素是 p 的元素
        */
        p:first-child {
          color: lime;
        }
        ```

- 组合选择器（Combinators）: 这种选择器可以作用于多个 HTML 元素，有多种组合方式
    - `A B {}` : A 元素的所有后代元素 B 都会起作用。
    - `A > B {}` : A 元素的直接子节点会起作用，也就是只适用于 A 节点的第一层所有的子节点。
    - `A + B {}` : 匹配 A 的下一个兄弟节点，AB具有相同的父节点，并且 B 紧跟在 A 的后面；
    - `A ~ B {}` : B是 A 之后的任意一个（所有）兄弟节点。
    - `A, B {}`：A 和 B 元素具有同一规则的 CSS 样式，不同元素使用逗号隔开。

### 伪选择器

1. 伪类选择器：作用是选中某个元素中符合某些条件的元素。作用于现有元素，相当于给现有元素添加某些属性。使用单个冒号 `:`

    ```css
    :first-child
    :not
    :nth-child()
    :only-child()
    :root()
    :disabled
    ```

2. 伪元素选择器：作用就是给现有元素添加某些新的内容，就好比给某个元素添加了一个新的标签，使用2个冒号 `::`

    ```css
    ::first-letter 表示对首字母进行操作
    ::first-line 对首行内容进行操作
    ::before 给已知元素的前面拼接新的内容
    ::after 给已知元素的后面拼接新的内容
    ```

### @规则

@规则在CSS中用于传递元数据、条件信息或其他描述性信息。它们以at符号（@）开头，后跟一个标识符来说明它是什么类型的规则，然后是某种类型的语法块，以分号（；）结尾。由标识符定义的每种类型的 at 规则都有其自己的内部语法和语义。

```css
@charset and @import (metadata)
@media or @document (条件，嵌套申明)
@font-face (描述信息)
```

下面这个 CSS 只适用于屏幕超过 800px 的设备：

```css
@media (min-width: 801px) {
  body {
    margin: 0 auto;
    width: 800px;
  }
}
```

`@media` 语法

```css
@media mediaType and|not|only (media feture) {
  // css
}
```

### border

- 简写属性，包含 border-width, border-style, border-color。
- `border-width`：表示边框的宽度，可以分别设置上下左右边框为不同的宽度，比如 border-bottom-width；
- `border-style`: 表示边框的样式，可以分别设置上下左右边框为不同的样式，比如 border-bottom-style，可以取下面几种值：node、hidden、dotted、dashed、solid 等；
- `border-color`：表示边框的颜色，可以分别设置上下左右边框为不同的颜色。

### 一些文字属性

font-size: 文字大小；

font-weight：字重，字体粗细，可以这样理解吧；

color：字体颜色；

text-align：字体对齐方式；

text-decoration: 文字修饰，比如下划线，删除线；

letter-spacing: 文字间距；

line-height: 行高；

font-style:  文字样式，比如斜体；

### 盒子模型

两种盒子类型

1. 块级盒子（block）
    - 尽可能扩大可利用的空间
    - 独占一行，也就说一个块级元素占一行
    - 可以使用 width 和 height 属性
    - 使用 padding、margin 和 border 会影响其它元素的位置
2. 行内盒子（inline）
    - 不会单行显示，除非一行没有足够多的空间，它会一个接一个地排列；
    - width 和 height 属性不起作用，如果给 span 标签设置 width 或 height 时，发现无效；
    - padding、margin 和 border 会起作用，但不会影响其它元素。

通过 `display` 修改盒子的显示方式

```css
.title {
    display: inline;
}
```

盒模型

![Untitled 1](https://user-images.githubusercontent.com/3297411/129540095-2a436855-1b09-4423-9b72-1fdab450c68e.png)

- margin（外边距）：它表示盒子之间的距离，可以通过 margin-top、margin-bottom、margin-left、margin-right 来控制各个方向的边距，**它们可以为负值**；
- border（边框）：表示盒子的边框；
- padding（内边距）：表示与内容之间的距离；
- content（内容）：表示内容的大小；

模式

1. 标准的盒子模型

    对于这种盒子模式，给它设置的 width 和 height 是 content 的宽高，当给盒子添加 padding 和 border 的时候，会增加盒子的整体大小。「外边距不会计入盒子的大小，它只是表示外部的边距」。

2. 诡异盒子模型（The alternative CSS box model）

    对于这种盒子模式，给它设置的 width 和 height 是盒子的宽高，也就是说内容 content 的宽需要减去 border 和 padding 的宽。

谷歌浏览器默认的是标准的盒模型，可以通过：

```css
box-sizing: border-box;
```

来修改盒模型为诡异盒模型。

### display

1. `display：inline`
2. `display：block`
3. `display：inline-block` 

    这种布局方式结合了 inline 和 block 这两种元素的特性，它与块级元素不同的是：元素不会单独占用一行；相同的是：可以使用 width 和 height，可以通过 padding、margin 和 border 来控制元素的显示位置。

    说白了就是除了不会单独占一行，其余的与块级元素一致。

4. `display：none` 隐藏元素
5. `display：flex` 一维
6. `display：grid` 二维

### 使用图片

1. 设置背景图

    ```css
    		background-color: antiquewhite;
        background-image: url('./logo_suyan.png');
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
    ```

    - background-postion: 表示背景图的起始位置；
        - background-postion： `top | left | bottom | right`，在某个边缘的位置，另一个维度为 50%。比如 top，背景图的起始位置为顶部，在X轴方向为 50%，居中显示；
        - background-postion：center，居中背景图；
        - background-postion：25% 75%，设置基于背景区域的开始位置，可以为负值；
        - background-postion-x：背景在 x 轴上的位置；
        - background-postion-y：背景在 y 轴上的位置；
    - background-repeat: 背景的重复方式， `no-repat` 不重复， `repeat` 重复， `repat-x` X轴上重复，还有其它关键字。
    - background-size: 背景图的大小；
2. `img` 标签

    行内（inline）元素

    ```html
    <img class="logo" src="./images/1.png" alt="图片">
    ```

    ```css
    .logo {
    		/* 表示设置图片的宽度，如果只设置宽度，那么 img 标签的高度会根据图片的大小进行等比缩放。
           只设置高度也是同样的道理。
           如果即设置了高度又设置了宽度，那么图片的高度和宽度即为设置的宽高。 */
        width: 30px;
        /* 指定行内元素的垂直对齐方式 */
        vertical-align: middle;
    }
    ```

### 显示多行文字

text-overflow 和 -webkit-line-clamp

```css
.singal-line {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}
```

```css
.two-line {
    display: -webkit-box;
    overflow: hidden;
    text-overflow: ellipsis;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}
```

text-overflow：只对块级元素起作用，表示对超出指定区域的内容该如何显示

- ellipsis：以 ... 省略号显示
- clip截断显示

-webkit-box：webkit 的 CSS 扩展属性

### CSS权重

![Untitled 2](https://user-images.githubusercontent.com/3297411/129540137-817a8c61-d9e3-4763-b984-b6a89f02f5de.png)

- `*`：通用选择器，权重最低，就是 0，第 1 张图就是此意；
- div、li>ul、body：元素选择器，有几个值权重值就是几。li>ul 是两个元素，> 号不会干扰权重计算；第 2、3、4张图能看懂了吧，就是元素选择器，1个元素选择器就是 0-0-1，12个元素选择器就是 0-0-12；
- `.myClass, [type=chekbox], :only-of-type` : 类、属性、伪类选择器。第 5 张图，一个类选择器，权重值表示为 0-1-0；5-15张图能看懂了吧；
- `#myDiv`：id选择器，一条鲨鱼，权重比较高，权重值为 1-0-0；`
- `style`：权重值更高，权重值为 1-0-0-0；
- `!important`: 无敌，我是老大，告诉浏览器必须使用我定义的属性；

![Untitled 3](https://user-images.githubusercontent.com/3297411/129540180-af9db964-ba31-4349-ba31-d271eba84078.png)

- `g`：直接在元素中使用属性，权重最高，可以看做 1-0-0-0；
- `z`：id选择器，权重次子，可以看做 0-1-0-0；
- `y`：类、伪类、属性选择器，权重低，可以看做 0-0-1-0；
- `x`：元素、伪元素选择器，权重最低，可以看做 0-0-0-1；

### 动画

主要有两种方式

- animation：CSS动画，可设置不同帧的动效；
- transition：这种属于过渡动画，也就是说在修改某些 CSS 属性的时候，属性会有一个渐变的过程。

1. animation
- animation-name: 动画的名字，这个是通过 `@keyframes` 定义的名字。 `@keyframes` 指定某一帧的动画如何变化，可通过 % 来控制各个阶段的属性值
- animation-duration：动画的持续时间；
- animation-delay：动画开始时的延迟时间；
- animation-iteration-count：动画循环次数；
- animation-direction：动画的方向，比如 alternate 表示先正向后逆序，nomal 正向，reverse 逆序；
- animation-timing-function：动画的时间曲线，它的值有 ease、ease-in、ease-out、ease-in-out、linear；
- animation-fill-mode：动画执行后的填充模式，它的值有 forwards、backwards、none、both；

```css
        .move-box-animation {
            /* animation: name duration timing-function delay iteration-count direction fill-mode; */
            /* 名字，为 @keyframes 的名字 */
            animation-name: move;
            /*  动画的时间 */
            animation-duration: 5s;
            /* 动画执行函数 */
            animation-timing-function: ease-in-out;
            /* 动画延迟时间 */
            animation-delay: 1s;
            /* 动画重复次数 */
            animation-iteration-count: 10;
            /* 动画的方向，先正向后逆向 */
            animation-direction: alternate;
            /* 动画执行后的填充模式 */
            animation-fill-mode: backwards;
            /* 动画的运行状态 */
            animation-play-state: running;
        }

        @keyframes move {
            0% {
                left: 0;
                top: 0;
            }

            25% {
                left: 100px;
                top: 0;
            }

            50% {
                left: 100px;
                top: 100px;
            }

            75% {
                left: 0;
                top: 100px;
            }

            100% {
                left: 0;
                top: 0;
            }
        }
```

1. transition
- 过渡动画，修改某些属性的时候不会立刻生效，它会以动画的形式逐渐过渡到要设置的值
- transition-property: 指需要使用过渡动画的属性，这里设置了背景色，高度和宽度。也可以通过关键字 all 设置所有的属性；
- transition-duration: 动画持续的时间，可以单独控制某个属性的时间， transition-duration：1.8s, 1.0s, 1.0s 表示修改 background-color 需要 1.8s, 修改 height 需要 1.0s,  修改 width 需要 1.0s;
- transition-delay：动画开始时需要延迟多长时间才开始执行；
- transition-timing-function：表示动画执行时的时间函数，不同函数走过的曲线不一样；

```css
.move-transition {
    /* transition-property: all; */
    transition-property: background-color, height, width;
    transition-duration: 1.8s, 1.0s, 1.0s;
    transition-delay: 0.1s;
    transition-timing-function: linear;
}
```

### 长度单位

1. 相对单位：相对单位指它的尺寸是相对于另外一个元素的尺寸。常用的是 em、rem、vh、vw、vmin、vmax。
    - em: 它是相对于「自身或父元素」的 font-size 来计算自身的尺寸
    - rem（font size of root element）: 这个单位是依据「根元素 html 标签」的 font-size 来计算最终的值，这个单位对移动端web开发十分实用，通过设置 html 的 font-size 来等比缩放元素的大小。
    - **vw（viewport width）**，可视区域宽度，比如设置 50vw，相当于可视区域宽度的一半；
    - **vh（viewport height）**，可视区域高度，比如设置 50vh，相当于可视区域高度的一半；
    - **vmax**: vw 和 vh 中最大的；
    - **vmin**: vw 和 vh 中最小的；
2. 绝对单位
    - 像素 px， cm等
3. 时间单位
    - s
    - ms

### 易复用、易维护、结构清晰的 CSS

less，sass


> GitHub repo: [qiwihui/blog](https://github.com/qiwihui/blog)
>
> Follow me: [@qiwihui](https://github.com/qiwihui)
>
> Site: [QIWIHUI](https://qiwihui.com)

