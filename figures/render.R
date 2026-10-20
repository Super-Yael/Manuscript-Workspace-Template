source("workflow/common.R")
a <- readRDS(project$summary)
x <- a$data
s <- a$summary
ensure_parent(project$figure)
pdf(project$figure, width = 6.4, height = 4.3, family = "Helvetica", useDingbats = FALSE)
par(mar = c(4, 4.5, 2, 1), las = 1, bty = "l")
colors <- c("#296A91", "#C66B35")
ylim <- range(x$outcome)
pad <- max(diff(ylim) * 0.15, 0.1)
plot(NA, xlim = c(0.5, 2.5), ylim = ylim + c(-pad, pad), xaxt = "n",
     xlab = "", ylab = "Outcome (arbitrary units)")
axis(1, at = 1:2, labels = project$groups)
for (i in seq_along(project$groups)) {
  y <- x$outcome[x$group == project$groups[i]]
  points(i + seq(-0.09, 0.09, length.out = length(y)), y, pch = 21,
         bg = adjustcolor(colors[i], 0.7), col = colors[i], cex = 1.15)
  segments(i - 0.16, s$mean[i], i + 0.16, s$mean[i], col = "#222222", lwd = 2.5)
}
legend("topleft", legend = "Points: samples; bars: group means", bty = "n", cex = 0.8)
invisible(dev.off())
