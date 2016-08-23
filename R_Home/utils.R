library(ggplot2)

mac_font = function(font = "HiraginoSansGB-W3"){
    theme(text=element_text(family = font))
}

statistics <- function(df){
    target = levels(df$category)
    
    categorys <- function(value){
        subset(df, category == value)
    }
    
    counts = sapply(target, function(x){length(categorys(x)$project)})
    funded_all = sapply(target, function(x){sum(categorys(x)$funded, na.rm = TRUE)})
    goal_median = sapply(target, function(x){median(categorys(x)$goal, na.rm = TRUE)})
    goal_mean = sapply(target, function(x){mean(categorys(x)$goal, na.rm = TRUE)})
    goal_max = sapply(target, function(x){max(categorys(x)$goal, na.rm = TRUE)})
    completion_median = sapply(target, function(x){median(categorys(x)$progress, na.rm = TRUE)})
    completion_max = sapply(target, function(x){max(categorys(x)$progress, na.rm = TRUE)})
    supports_median = sapply(target, function(x){median(categorys(x)$supports, na.rm = TRUE)})
    supports_mean = sapply(target, function(x){mean(categorys(x)$supports, na.rm = TRUE)})
    supports_max = sapply(target, function(x){max(categorys(x)$supports, na.rm = TRUE)})
    
    create_frame <- function(val, item="其他", type="总数"){
        data.frame(类别=target, 统计项=as.factor(item), 统计值=val, 统计类型=as.factor(type))
    }
    
    count_frame = create_frame(counts, item = "项目")
    funded_frame = create_frame(funded_all, item = "筹集资金")
    goal_frame = rbind(create_frame(goal_max, item = "筹集目标", type = "最大值"), 
                       create_frame(goal_mean, item = "筹集目标", type = "均值"),
                       create_frame(goal_median, item = "筹集目标", type = "中位值"))
    completion_frame = rbind(create_frame(completion_max, item = "完成度", type = "最大值"),
                             create_frame(completion_median, item = "完成度", type = "中位值"))
    support_frame = rbind(create_frame(supports_max, item = "支持数", type = "最大值"), 
                          create_frame(supports_mean, item = "支持数", type = "均值"),
                          create_frame(supports_median, item = "支持数", type = "中位值"))
    
    frame = rbind(count_frame, funded_frame, goal_frame, completion_frame, support_frame)
    row.names(frame) <- 1:length(frame$统计值)
    frame$类别 = as.factor(frame$类别)
    frame
}

pie_graph_overall <- function(df, item="项目", postfix = FALSE){
    frame = subset(df, 统计项==item)
    frame = frame[order(frame$统计值,decreasing = TRUE),]
    
    options(digits = 10)
    
    graph_label = paste(frame$类别, "(")
    if (postfix) {
        graph_label = paste(graph_label, 
                            formatC(as.numeric(frame$统计值 / 10000), format = "f", digits = 2, big.mark = ','), 
                            "万)", sep = " ")
    }
    else {
        graph_label = paste(graph_label, 
                            formatC(as.numeric(frame$统计值), format = 'f', digits = 0, big.mark = ','), 
                            ")", sep = " ")
    }
    
    p = ggplot(data = frame, aes(x="", y=统计值, fill=类别))
    p = p + geom_bar(stat = "identity", width = 1)
    p = p + coord_polar(theta = "y")
    p = p + labs(x = "", y = "", title = "")
    p = p + theme(axis.ticks = element_blank())
    p = p + theme(legend.title = element_blank())
    p = p + theme(axis.text.x = element_blank())
    p + scale_fill_discrete(breaks = frame$类别, labels = graph_label) 
}

pie_graph_winner <- function(data, from="众筹项目", postfix=FALSE){
    df = subset(data, 数据==from)
    tmp = df[order(df$总值,decreasing = TRUE),]
    graph_label = paste(tmp$发起人, "(")
    if (postfix) {
        graph_label = paste(graph_label, 
                            formatC(as.numeric(tmp$总值 / 10000), format = "f", digits = 2, big.mark = ','), 
                            "万)", sep = " ")
    }
    else {
        graph_label = paste(graph_label, 
                            formatC(as.numeric(tmp$总值), format = 'f', digits = 0, big.mark = ','), 
                            ")", sep = " ")
    }
    
    options(digits = 10)
    
    p = ggplot(data = tmp, aes(x="", y=总值, fill=发起人))
    p = p + geom_bar(stat = "identity", width = 1)
    p = p + coord_polar(theta = "y")
    p = p + labs(x = "", y = "", title = "")
    p = p + theme(axis.ticks = element_blank())
    p = p + theme(legend.title = element_blank())
    p = p + theme(axis.text.x = element_blank())
    p + scale_fill_discrete(breaks = tmp$发起人, labels = graph_label)
}

bar_graph_overall <- function(df, item="筹集目标", single=FALSE){
    frame = subset(df, 统计项==item & 统计类型 != "最大值")
    
    p = ggplot(data = frame, mapping = aes(x = 类别, y = 统计值, fill = 统计类型))
    if (single) {
        p = ggplot(data = frame, mapping = aes(x = 类别, y = 统计值))
    }
    p = p + geom_bar(stat = "identity", position = "dodge")
    p + labs(y=item)
}

bar_graph_winner <- function(df, from="众筹项目"){
    frame = subset(df, 数据==from)
    frame = frame[order(-frame$总值), ]
    p = ggplot(data = frame, mapping = aes(x = reorder(发起人, 总值), y = 总值))
    p = p + geom_bar(stat = "identity")
    p = p + geom_text(aes(label=总值), hjust=1.6, size=4, color="white")
    p = p + coord_flip()
    p + labs(x=from)
}

get_project_winner <- function(df) {
    winners = summary(df$sponsor)[1:10]
    target = names(winners)
    frame = subset(df, sponsor %in% target)
    
    sponsors <- function(value){
        subset(frame, sponsor == value)
    }
    
    funded_quantity = sapply(target, function(x){sum(sponsors(x)$funded)})
    supporters_quantity = sapply(target, function(x){sum(sponsors(x)$supports)})
    
    quantity = data.frame(总值 = winners, 数据 = "众筹项目", 发起人=target)
    funding = data.frame(总值=funded_quantity, 数据='众筹资金', 发起人=target)
    supporter = data.frame(总值=supporters_quantity, 数据="支持者", 发起人=target)

    rst = rbind(quantity, funding, supporter)
    rst
}

get_valuable_projects <- function(df){
    frame = cbind(df, funded_per_support=round(df$funded / df$supports, 1))
    frame = frame[order(-frame$funded_per_support), ]
    frame = head(frame, 8)
    
    projects = paste(frame$project, "(", frame$sponsor, ")")
    
    fps = data.frame(最贵的项目=projects, value=frame$funded_per_support, Name="支持者赞助均值")
    supports = data.frame(最贵的项目=projects, value=frame$supports, Name="支持者数量")
    rst = rbind(fps, supports)
    
    p = ggplot(data = rst, mapping = aes(y = value, fill=最贵的项目))
    p = p + facet_wrap(~Name,  scales = "free_y")
    p = p + geom_bar(aes(x = reorder(最贵的项目, value)), stat = "identity")
    p = p + geom_text(aes(x = reorder(最贵的项目, value), label=value), vjust=-0.8, size=3.6)
    p = p + labs(x = "", y = "", title = "")
    p = p + theme(axis.ticks = element_blank())
    p = p + theme(axis.text.x = element_blank())
    p
}