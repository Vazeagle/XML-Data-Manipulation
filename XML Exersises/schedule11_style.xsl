<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
		<xsl:template match="/">
			<html>
				<body>
					<h2>Schedule</h2>
					<table border="1">
						<tr bgcolor="#9acd32">
							<th>Title</th>
							<th>Professor</th>
							<th>Day</th>
						</tr>
						<xsl:for-each select="//Lesson/Lecture[Day='Monday']">
						<tr bgcolor="red">
							<td><xsl:value-of select="../Title"/></td>
							<td><xsl:value-of select="../Professor"/></td>
							<td><xsl:value-of select="Day"/></td>
						</tr>
						</xsl:for-each>
						
						<xsl:for-each select="//Schedule/Lesson/Lecture[Day='Tuesday']">
						<tr bgcolor="blue">
							<td><xsl:value-of select="../Title"/></td>
							<td><xsl:value-of select="../Professor"/></td>
							<td><xsl:value-of select="Day"/></td>
						</tr>
						</xsl:for-each>
						
						<xsl:for-each select="//Schedule/Lesson/Lecture[Day='Wednesday']">
						<tr bgcolor="yellow">
							<td><xsl:value-of select="../Title"/></td>
							<td><xsl:value-of select="../Professor"/></td>
							<td><xsl:value-of select="Day"/></td>
						</tr>
						</xsl:for-each>
						
						<xsl:for-each select="//Schedule/Lesson/Lecture[Day='Thursday']">
						<tr bgcolor="cyan">
							<td><xsl:value-of select="../Title"/></td>
							<td><xsl:value-of select="../Professor"/></td>
							<td><xsl:value-of select="Day"/></td>
						</tr>
						</xsl:for-each>
						
						<xsl:for-each select="//Schedule/Lesson/Lecture[Day='Friday']">
						<tr bgcolor="orange">
							<td><xsl:value-of select="../Title"/></td>
							<td><xsl:value-of select="../Professor"/></td>
							<td><xsl:value-of select="Day"/></td>
						</tr>
						</xsl:for-each>
						
						<xsl:for-each select="//Schedule/Lesson/Lecture[Day='Saturday']">
						<tr bgcolor="purple">
							<td><xsl:value-of select="../Title"/></td>
							<td><xsl:value-of select="../Professor"/></td>
							<td><xsl:value-of select="Day"/></td>
						</tr>
						</xsl:for-each>
						
						<xsl:for-each select="//Schedule/Lesson/Lecture[Day='Sunday']">
						<tr bgcolor="pink">
							<td><xsl:value-of select="../Title"/></td>
							<td><xsl:value-of select="../Professor"/></td>
							<td><xsl:value-of select="Day"/></td>
						</tr>
						</xsl:for-each>
						
						
					</table>
				</body>
			</html>
		</xsl:template>
	</xsl:stylesheet>