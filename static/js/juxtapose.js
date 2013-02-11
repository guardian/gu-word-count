var juxtapose = function(text, interval, spacer) {
    var juxtaposeRecur = function(input, acc, output) {
        if(input.length < 1) {
            //console.log(input, ":", output, ":", acc);
            
            if(acc.length > 0) {
                return acc + output;
            }
            
            return output;
        }
        
        if(acc.length == interval) {
            output = spacer + acc + output;
            acc = "";
        }
        
        var c = input[input.length - 1];
        acc = c + acc;
        //console.log(input, output, acc, c);
        
        input = input.substr(0, input.length - 1);
            
        return juxtaposeRecur(input, acc, output);
    };
    
    return juxtaposeRecur(text, "", "");
};
