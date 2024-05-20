function fn1(fn2) {
    setTimeout(function() {
        console.log(1);
        fn2 && typeof fn2 === 'function' && fn2();
    }, 1000);
}

function fn2(){
     console.log(2);
}

fn1();
fn2()