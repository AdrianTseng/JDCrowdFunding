library(ggplot2)

mac_font = function(font = "HiraginoSansGB-W3"){
    theme(text=element_text(family = font))
}

categorys <- function(value){
    subset(CrowdFunding, category == value)
}

statistics <- function(df){
    target = levels(df$category)
    counts = sapply(target, function(x){length(categorys(x)$project)})
    funded_all = sapply(target, function(x){sum(categorys(x)$funded)})
    goal_median = sapply(target, function(x){median(categorys(x)$goal)})
    goal_mean = sapply(target, function(x){mean(categorys(x)$goal)})
    goal_max = sapply(target, function(x){max(categorys(x)$goal)})
    completion_median = sapply(target, function(x){median(categorys(x)$progress)})
    completion_max = sapply(target, function(x){max(categorys(x)$progress)})
    supports_median = sapply(target, function(x){median(categorys(x)$supports)})
    supports_mean = sapply(target, function(x){mean(categorys(x)$supports)})
    supports_max = sapply(target, function(x){max(categorys(x)$supports)})
    
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

pie_graph <- function(df, item="项目"){
    frame = subset(df, 统计项==item)
    
    frame = frame[order(frame$统计值,decreasing = TRUE),]
    graph_label = paste(frame$类别, "(", round(frame$统计值 / sum(frame$统计值) * 100, 2), "%)  ")
    
    p = ggplot(data = frame, aes(x="", y=统计值, fill=类别))
    p = p + geom_bar(stat = "identity", width = 1)
    p = p + coord_polar(theta = "y")
    p = p + labs(x = "", y = "", title = "")
    p = p + theme(axis.ticks = element_blank())
    p = p + theme(legend.title = element_blank())
    p = p + theme(axis.text.x = element_blank())
    p + scale_fill_discrete(breaks = frame$类别, labels = graph_label) 
}

bar_graph <- function(df, item="筹集目标"){
    frame = subset(df, 统计项==item & 统计类型 != "最大值")
    
    p = ggplot(data = frame, mapping = aes(x = 类别, y = 统计值, fill = 统计类型))
    p = p + geom_bar(stat = "identity", position = "dodge")
    p + labs(y=item)
}
